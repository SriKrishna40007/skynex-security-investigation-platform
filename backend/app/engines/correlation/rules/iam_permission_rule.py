from __future__ import annotations

import re
from typing import Any

from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.correlation.rules.base import RelationshipRule


class IAMPermissionRule(RelationshipRule):
    """
    Discovers security-semantic IAM permission relationships.

    V1 intentionally handles the strongest deterministic case:
    an IAM role policy containing both Action="*" and Resource="*".

    The resulting allows_action relationship connects the policy to
    canonical resources that the wildcard policy can act upon.
    """

    IAM_POLICY_TYPES = frozenset(
        {
            "aws_iam_role_policy",
            "aws_iam_policy",
        }
    )

    def discover(
        self,
        resources: list[Resource],
    ) -> list[Relationship]:
        relationships: list[Relationship] = []

        targets = [
            resource
            for resource in resources
            if resource.type.startswith("aws_")
            and resource.type not in self.IAM_POLICY_TYPES
        ]

        for policy in resources:
            if policy.type not in self.IAM_POLICY_TYPES:
                continue

            policy_text = self._policy_text(policy.metadata)

            if not self._is_unrestricted_wildcard_policy(policy_text):
                continue

            for target in targets:
                relationships.append(
                    Relationship(
                        source_id=policy.id,
                        target_id=target.id,
                        relationship_type="allows_action",
                        metadata={
                            "action": "*",
                            "resource": "*",
                            "reason": "unrestricted IAM wildcard policy",
                        },
                    )
                )

        return relationships

    @staticmethod
    def _policy_text(metadata: dict[str, Any]) -> str:
        policy = metadata.get("policy", "")
        return str(policy)

    @staticmethod
    def _is_unrestricted_wildcard_policy(policy_text: str) -> bool:
        """
        Recognize the deterministic Terraform SDK representation of:

            Action   = "*"
            Resource = "*"

        This is intentionally conservative. V1 does not attempt to parse
        arbitrary IAM policy expressions.
        """

        action_match = re.search(
            r'Action\s*=\s*"?\*"?',
            policy_text,
        )

        resource_match = re.search(
            r'Resource\s*=\s*"?\*"?',
            policy_text,
        )

        return bool(action_match and resource_match)

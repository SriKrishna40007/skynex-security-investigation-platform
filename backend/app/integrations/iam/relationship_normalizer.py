from __future__ import annotations

from typing import Any

from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource


class IAMRelationshipNormalizer:
    """
    Converts IAM policy authorization evidence into canonical SKYNEX
    relationships.

    The normalizer represents only relationships directly supported by
    policy evidence. It does not infer principals, trust relationships,
    or attack paths that are not present in the supplied policy.
    """

    def normalize_policy_relationships(
        self,
        policy_data: dict[str, Any],
        resources: list[Resource],
    ) -> list[Relationship]:
        resource_lookup = {
            resource.metadata.get("arn"): resource
            for resource in resources
            if resource.metadata.get("arn")
        }

        policy_resources = [
            resource for resource in resources if resource.type == "iam_policy"
        ]

        if not policy_resources:
            return []

        policy_resource = policy_resources[0]

        statements = policy_data.get("Statement", [])

        if isinstance(statements, dict):
            statements = [statements]

        relationships: list[Relationship] = []
        seen: set[tuple[str, str, str]] = set()

        for statement_index, statement in enumerate(statements):
            if not isinstance(statement, dict):
                continue

            effect = statement.get("Effect")

            if effect != "Allow":
                continue

            actions = self._as_list(statement.get("Action"))
            targets = self._as_list(statement.get("Resource"))

            for target_arn in targets:
                if not isinstance(target_arn, str):
                    continue

                if target_arn == "*":
                    continue

                target_resource = resource_lookup.get(target_arn)

                if target_resource is None:
                    continue

                relationship_type = self._relationship_type(actions)

                key = (
                    policy_resource.id,
                    target_resource.id,
                    relationship_type,
                )

                if key in seen:
                    continue

                seen.add(key)

                relationships.append(
                    Relationship(
                        source_id=policy_resource.id,
                        target_id=target_resource.id,
                        relationship_type=relationship_type,
                        metadata={
                            "effect": effect,
                            "actions": actions,
                            "statement_index": statement_index,
                            "source": "iam_policy",
                        },
                    )
                )

        return relationships

    @staticmethod
    def _relationship_type(
        actions: list[str],
    ) -> str:
        normalized = {action.lower() for action in actions if isinstance(action, str)}

        if "sts:assumerole" in normalized:
            return "allows_assume_role"

        return "allows_action"

    @staticmethod
    def _as_list(
        value: Any,
    ) -> list[Any]:
        if value is None:
            return []

        if isinstance(value, list):
            return value

        return [value]

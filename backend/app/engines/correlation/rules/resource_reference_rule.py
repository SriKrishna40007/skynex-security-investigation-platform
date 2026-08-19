from __future__ import annotations

from typing import Any

from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.correlation.rules.base import RelationshipRule


class ResourceReferenceRule(RelationshipRule):
    """
    Discovers semantic infrastructure relationships from Terraform
    resource references.
    """

    RELATIONSHIP_TYPES = {
        "vpc_id": "belongs_to",
        "subnet_id": "deployed_in",
        "security_group_id": "protected_by",
        "security_group_ids": "protected_by",
        "vpc_security_group_ids": "protected_by",
        "route_table_id": "routed_by",
        "network_interface_id": "attached_to",
        "iam_instance_profile": "uses",
    }

    def discover(
        self,
        resources: list[Resource],
    ) -> list[Relationship]:
        relationships: list[Relationship] = []

        resource_lookup = {resource.id: resource for resource in resources}

        for resource in resources:
            references = resource.metadata.get("references", [])

            for reference in references:
                if reference not in resource_lookup:
                    continue

                relationship_type = self._relationship_type(
                    resource.metadata,
                    reference,
                )

                relationships.append(
                    Relationship(
                        source_id=resource.id,
                        target_id=reference,
                        relationship_type=relationship_type,
                    )
                )

        return relationships

    def _relationship_type(
        self,
        metadata: dict[str, Any],
        reference: str,
    ) -> str:
        """
        Determine the semantic relationship represented by a Terraform
        reference.

        The lookup examines the actual Terraform attribute containing the
        reference rather than relying on the generic `references` metadata.
        """

        for attribute, value in metadata.items():
            if attribute == "references":
                continue

            if self._contains_reference(value, reference):
                return self.RELATIONSHIP_TYPES.get(
                    attribute,
                    "references",
                )

        return "references"

    @staticmethod
    def _contains_reference(
        value: Any,
        reference: str,
    ) -> bool:
        """Recursively determine whether a Terraform value contains a resource reference."""

        if isinstance(value, str):
            return reference in value

        if isinstance(value, dict):
            return any(
                ResourceReferenceRule._contains_reference(
                    item,
                    reference,
                )
                for item in value.values()
            )

        if isinstance(value, list):
            return any(
                ResourceReferenceRule._contains_reference(
                    item,
                    reference,
                )
                for item in value
            )

        return False

from __future__ import annotations

from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.correlation.rules.base import RelationshipRule


class ResourceReferenceRule(RelationshipRule):
    """
    Discovers infrastructure relationships from Terraform references.
    """

    RELATIONSHIP_TYPES = {
        "vpc_id": "belongs_to",
        "subnet_id": "deployed_in",
        "security_group_id": "protected_by",
        "security_group_ids": "protected_by",
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
            references = resource.metadata.get(
                "references",
                [],
            )

            for reference in references:
                if reference not in resource_lookup:
                    continue

                relationship_type = "references"

                for attribute, value in resource.metadata.items():
                    if reference not in str(value):
                        continue

                    relationship_type = self.RELATIONSHIP_TYPES.get(
                        attribute,
                        "references",
                    )

                    break

                relationships.append(
                    Relationship(
                        source_id=resource.id,
                        target_id=reference,
                        relationship_type=relationship_type,
                    )
                )

        return relationships

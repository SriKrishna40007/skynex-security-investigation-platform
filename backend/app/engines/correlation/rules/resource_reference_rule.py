from __future__ import annotations

from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.correlation.rules.base import RelationshipRule


class ResourceReferenceRule(RelationshipRule):
    """
    Discovers relationships based on explicit resource references.

    Expected metadata format:

    metadata = {
        "references": [
            "aws_security_group.web",
            "aws_iam_role.app"
        ]
    }
    """

    def discover(
        self,
        resources: list[Resource],
    ) -> list[Relationship]:
        relationships: list[Relationship] = []

        resource_lookup = {
            resource.id: resource
            for resource in resources
        }

        for resource in resources:
            references = resource.metadata.get("references", [])

            for reference in references:
                if reference not in resource_lookup:
                    continue

                relationships.append(
                    Relationship(
                        source_id=resource.id,
                        target_id=reference,
                        relationship_type="references",
                    )
                )

        return relationships

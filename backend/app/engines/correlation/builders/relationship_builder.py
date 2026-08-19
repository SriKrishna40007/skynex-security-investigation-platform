from __future__ import annotations

from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.correlation.rules import (
    IAMPermissionRule,
    RelationshipRule,
    ResourceReferenceRule,
)


class RelationshipBuilder:
    """
    Builds canonical relationships from normalized SKYNEX resources.

    Relationship discovery operates on canonical resource evidence rather
    than provider-specific scanner output. This keeps downstream graph
    processing independent from Terraform, IAM, and future integrations.
    """

    def __init__(
        self,
        rules: list[RelationshipRule] | None = None,
    ) -> None:
        self._rules = rules or [
            ResourceReferenceRule(),
            IAMPermissionRule(),
        ]

    def build(
        self,
        resources: list[Resource],
    ) -> list[Relationship]:
        """
        Execute registered relationship-discovery rules and return
        deterministic, duplicate-free canonical relationships.
        """

        relationships: list[Relationship] = []
        seen: set[tuple[str, str, str]] = set()

        for rule in self._rules:
            discovered = rule.discover(resources)

            for relationship in discovered:
                key = (
                    relationship.source_id,
                    relationship.target_id,
                    relationship.relationship_type,
                )

                if key in seen:
                    continue

                seen.add(key)
                relationships.append(relationship)

        return relationships

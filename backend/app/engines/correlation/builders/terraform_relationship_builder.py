from __future__ import annotations

from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.correlation.rules import (
    RelationshipRule,
    ResourceReferenceRule,
)


class TerraformRelationshipBuilder:
    """
    Builds relationships between canonical Terraform resources.
    """

    def __init__(self) -> None:
        self._rules: list[RelationshipRule] = [
            ResourceReferenceRule(),
        ]

    def build(
        self,
        resources: list[Resource],
    ) -> list[Relationship]:
        """
        Execute all registered relationship discovery rules.
        """

        relationships: list[Relationship] = []

        for rule in self._rules:
            relationships.extend(rule.discover(resources))

        return relationships

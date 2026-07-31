from __future__ import annotations


class RelationshipSemantics:
    """
    Defines provider-neutral security semantics for canonical relationships.

    Graph algorithms must reason about canonical relationship meaning rather
    than the provider or integration that produced the relationship.
    """

    SECURITY_TRAVERSABLE_TYPES = frozenset(
        {
            "references",
            "connects",
            "belongs_to",
            "deployed_in",
            "protected_by",
            "routed_by",
            "attached_to",
            "uses",
            "allows_assume_role",
            "allows_action",
        }
    )

    @classmethod
    def is_security_traversable(
        cls,
        relationship_type: str,
    ) -> bool:
        """
        Return whether a canonical relationship can participate in
        security-reachability analysis.
        """

        return relationship_type in cls.SECURITY_TRAVERSABLE_TYPES

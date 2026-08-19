from __future__ import annotations


class RelationshipSemantics:
    """
    Defines provider-neutral security semantics for canonical relationships.

    Canonical graph relationships preserve their discovered source -> target
    direction. Security traversal may interpret some relationships in the
    opposite direction when compromise propagation requires it.
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

    REVERSE_PROPAGATION_TYPES = frozenset(
        {
            "protected_by",
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

    @classmethod
    def propagates_forward(
        cls,
        relationship_type: str,
    ) -> bool:
        """
        Return whether security propagation follows the canonical
        source -> target direction.
        """

        return (
            cls.is_security_traversable(relationship_type)
            and relationship_type not in cls.REVERSE_PROPAGATION_TYPES
        )

    @classmethod
    def propagates_reverse(
        cls,
        relationship_type: str,
    ) -> bool:
        """
        Return whether security propagation follows the canonical
        target -> source direction.
        """

        return relationship_type in cls.REVERSE_PROPAGATION_TYPES

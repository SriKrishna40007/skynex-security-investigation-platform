from __future__ import annotations

from dataclasses import dataclass

from app.engines.graph.models import KnowledgeGraph


@dataclass(frozen=True, slots=True)
class AttackPathRisk:
    """
    Provider-neutral semantic assessment of a discovered attack path.
    """

    severity: str
    description: str


class AttackPathSemanticRiskPolicy:
    """
    Evaluates the security significance of a discovered graph path.

    The policy reasons exclusively about canonical relationship semantics.
    It must not depend on AWS, Terraform, IAM, ARNs, or integration-specific
    implementation details.
    """

    _RELATIONSHIP_WEIGHTS = {
        "allows_assume_role": 4,
        "allows_action": 3,
        "connects": 2,
        "references": 2,
        "uses": 2,
        "attached_to": 2,
        "routed_by": 2,
        "protected_by": 1,
        "deployed_in": 1,
        "belongs_to": 1,
    }

    def evaluate(
        self,
        graph: KnowledgeGraph,
        nodes: list[str],
    ) -> AttackPathRisk:
        if len(nodes) < 2:
            return AttackPathRisk(
                severity="LOW",
                description="No attack path could be established.",
            )

        relationship_types = self._relationship_types(
            graph,
            nodes,
        )

        semantic_score = sum(
            self._RELATIONSHIP_WEIGHTS.get(
                relationship_type,
                0,
            )
            for relationship_type in relationship_types
        )

        hop_count = len(nodes) - 1

        # Relationship semantics are the primary risk signal.
        #
        # Path depth may increase exposure, but ordinary connectivity must
        # not become CRITICAL solely because several traversable edges are
        # chained together. Preserve the established three-hop connectivity
        # contract while still allowing semantic relationships such as
        # privilege transitions to carry greater weight.
        depth_bonus = max(hop_count - 2, 0)

        semantic_score += depth_bonus

        if semantic_score >= 8:
            return AttackPathRisk(
                severity="CRITICAL",
                description=(
                    "Attack path contains high-impact security relationships "
                    "and multiple opportunities for compromise propagation."
                ),
            )

        if semantic_score >= 4:
            return AttackPathRisk(
                severity="HIGH",
                description=(
                    "Attack path contains security-significant relationships "
                    "that can enable privileged or sensitive access."
                ),
            )

        if semantic_score >= 2:
            return AttackPathRisk(
                severity="MEDIUM",
                description=(
                    "Target is reachable through security-relevant "
                    "resource relationships."
                ),
            )

        return AttackPathRisk(
            severity="LOW",
            description=(
                "A graph path exists but does not contain sufficient "
                "security significance for elevated risk."
            ),
        )

    @staticmethod
    def _relationship_types(
        graph: KnowledgeGraph,
        nodes: list[str],
    ) -> list[str]:
        relationship_types: list[str] = []

        for source, target in zip(nodes, nodes[1:], strict=False):
            relationship_type = next(
                (
                    edge.relationship_type
                    for edge in graph.neighbors(source)
                    if edge.target == target
                ),
                None,
            )

            if relationship_type is not None:
                relationship_types.append(
                    relationship_type,
                )

        return relationship_types

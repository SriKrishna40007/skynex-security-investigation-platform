from __future__ import annotations

from app.engines.graph.models import KnowledgeGraph
from app.engines.graph.policies import RelationshipSemantics
from app.engines.graph.traversal.security_neighbor import SecurityNeighbor


class SecurityNeighborResolver:
    """
    Resolves security propagation neighbors from the canonical graph.

    Canonical graph direction remains unchanged. Security propagation may
    interpret selected relationships in reverse when their semantics require
    compromise propagation in that direction.

    IAM policy attachment is intentionally handled here rather than globally
    reversing all `references` relationships.
    """

    def resolve(
        self,
        graph: KnowledgeGraph,
        resource_id: str,
    ) -> list[SecurityNeighbor]:
        neighbors: list[SecurityNeighbor] = []

        current_node = graph.get_node(resource_id)

        # Canonical forward propagation.
        for edge in graph.neighbors(resource_id):
            if RelationshipSemantics.propagates_forward(
                edge.relationship_type,
            ):
                neighbors.append(
                    SecurityNeighbor(
                        resource_id=edge.target,
                        relationship_type=edge.relationship_type,
                        direction="forward",
                    )
                )

        # Explicit reverse propagation semantics.
        for edge in graph.edges:
            if edge.target != resource_id:
                continue

            if RelationshipSemantics.propagates_reverse(
                edge.relationship_type,
            ):
                neighbors.append(
                    SecurityNeighbor(
                        resource_id=edge.source,
                        relationship_type=edge.relationship_type,
                        direction="reverse",
                    )
                )

        # IAM security propagation:
        #
        # Canonical:
        #     aws_iam_role_policy -> references -> aws_iam_role
        #
        # Security propagation:
        #     aws_iam_role -> aws_iam_role_policy
        #
        # This is deliberately restricted to an IAM policy referencing an
        # IAM role. Ordinary Terraform references are not reversed.
        if current_node is not None:
            for edge in graph.edges:
                if edge.target != resource_id:
                    continue

                if edge.relationship_type != "references":
                    continue

                source_node = graph.get_node(edge.source)

                if source_node is None:
                    continue

                if (
                    source_node.resource_type
                    in {
                        "aws_iam_role_policy",
                        "aws_iam_policy",
                    }
                    and current_node.resource_type == "aws_iam_role"
                ):
                    neighbors.append(
                        SecurityNeighbor(
                            resource_id=edge.source,
                            relationship_type="references",
                            direction="reverse",
                        )
                    )

        return neighbors

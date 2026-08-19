from __future__ import annotations

from collections import deque

from app.domain.models.investigation import Investigation
from app.engines.blast_radius.base import BlastRadiusEngine
from app.engines.blast_radius.models import (
    BlastRadiusAnalysis,
    BlastRadiusImpact,
)
from app.engines.graph.algorithms import BreadthFirstTraversal
from app.engines.graph.models import KnowledgeGraph
from app.engines.graph.traversal import SecurityNeighborResolver


class DefaultBlastRadiusEngine(BlastRadiusEngine):
    """
    Calculates security-aware blast radius over the canonical knowledge graph.

    The legacy ``blast_radius`` list remains available for compatibility while
    ``blast_radius_analysis`` preserves richer propagation evidence.
    """

    def __init__(self) -> None:
        self._traversal = BreadthFirstTraversal()
        self._neighbors = SecurityNeighborResolver()

    def analyze(
        self,
        investigation: Investigation,
        compromised_resource: str,
    ) -> Investigation:
        graph: KnowledgeGraph = investigation.analysis["knowledge_graph"]

        reachable_resources = self._traversal.traverse(
            graph,
            compromised_resource,
        )

        investigation.analysis["blast_radius"] = reachable_resources

        investigation.analysis["blast_radius_analysis"] = self._build_analysis(
            graph,
            compromised_resource,
            reachable_resources,
        )

        return investigation

    @staticmethod
    def _build_analysis(
        graph: KnowledgeGraph,
        compromised_resource: str,
        reachable_resources: list[str],
    ) -> BlastRadiusAnalysis:
        """
        Build evidence explaining how compromise propagates through the graph.

        Only security-traversable canonical relationships participate in the
        evidence model. The calculation therefore remains aligned with the
        blast-radius traversal contract.
        """

        if graph.get_node(compromised_resource) is None:
            return BlastRadiusAnalysis(
                compromised_resource=compromised_resource,
                reachable_resources=(),
                impacts=(),
            )

        depths: dict[str, int] = {
            compromised_resource: 0,
        }

        relationship_paths: dict[str, tuple[str, ...]] = {
            compromised_resource: (),
        }

        queue = deque([compromised_resource])

        neighbors = SecurityNeighborResolver()

        while queue:
            current = queue.popleft()

            for neighbor in neighbors.resolve(
                graph,
                current,
            ):
                resource_id = neighbor.resource_id

                if resource_id in depths:
                    continue

                depths[resource_id] = depths[current] + 1
                relationship_paths[resource_id] = (
                    *relationship_paths[current],
                    neighbor.relationship_type,
                )

                queue.append(resource_id)

        impacts = tuple(
            BlastRadiusImpact(
                resource_id=resource_id,
                depth=depths[resource_id],
                relationship_types=relationship_paths[resource_id],
            )
            for resource_id in reachable_resources
            if resource_id in depths
        )

        return BlastRadiusAnalysis(
            compromised_resource=compromised_resource,
            reachable_resources=tuple(reachable_resources),
            impacts=impacts,
        )

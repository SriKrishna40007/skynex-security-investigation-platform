from __future__ import annotations

from collections import deque

from app.engines.graph.models import KnowledgeGraph
from app.engines.graph.traversal import SecurityNeighborResolver


class BreadthFirstTraversal:
    """
    Performs security-aware breadth-first traversal over a KnowledgeGraph.

    Canonical graph direction is preserved. Security relationship semantics
    determine whether propagation moves forward or reverse.
    """

    def __init__(self) -> None:
        self._neighbors = SecurityNeighborResolver()

    def traverse(
        self,
        graph: KnowledgeGraph,
        start_node: str,
    ) -> list[str]:
        if graph.get_node(start_node) is None:
            return []

        visited: set[str] = set()
        queue = deque([start_node])
        order: list[str] = []

        while queue:
            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)
            order.append(current)

            for neighbor in self._neighbors.resolve(
                graph,
                current,
            ):
                if neighbor.resource_id not in visited:
                    queue.append(neighbor.resource_id)

        return order

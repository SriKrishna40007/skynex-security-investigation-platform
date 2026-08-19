from __future__ import annotations

from collections import deque

from app.engines.graph.models import KnowledgeGraph
from app.engines.graph.traversal import SecurityNeighborResolver


class PathFinder:
    """
    Finds the shortest security-semantic path between two graph nodes.

    Canonical graph direction is preserved. SecurityNeighborResolver determines
    whether propagation follows an edge forward or in reverse according to
    relationship semantics.
    """

    def __init__(self) -> None:
        self._neighbors = SecurityNeighborResolver()

    def shortest_path(
        self,
        graph: KnowledgeGraph,
        start: str,
        target: str,
    ) -> list[str]:
        if graph.get_node(start) is None:
            return []

        if graph.get_node(target) is None:
            return []

        queue = deque([(start, [start])])
        visited: set[str] = set()

        while queue:
            current, path = queue.popleft()

            if current == target:
                return path

            if current in visited:
                continue

            visited.add(current)

            for neighbor in self._neighbors.resolve(
                graph,
                current,
            ):
                if neighbor.resource_id in visited:
                    continue

                queue.append(
                    (
                        neighbor.resource_id,
                        path + [neighbor.resource_id],
                    )
                )

        return []

from __future__ import annotations

from collections import deque

from app.engines.graph.models import KnowledgeGraph


class PathFinder:
    """
    Finds the shortest path between two nodes using
    Breadth-First Search (BFS).
    """

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

            for edge in graph.neighbors(current):

                if edge.target not in visited:
                    queue.append(
                        (
                            edge.target,
                            path + [edge.target],
                        )
                    )

        return []

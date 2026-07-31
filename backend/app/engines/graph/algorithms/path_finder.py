from __future__ import annotations

from collections import deque

from app.engines.graph.models import KnowledgeGraph
from app.engines.graph.policies import RelationshipSemantics


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
                if not RelationshipSemantics.is_security_traversable(
                    edge.relationship_type
                ):
                    continue

                if edge.target not in visited:
                    queue.append(
                        (
                            edge.target,
                            path + [edge.target],
                        )
                    )

        return []

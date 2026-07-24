from collections import deque

from app.engines.graph.models import KnowledgeGraph


class PathFinder:
    """Finds the shortest path between two nodes."""

    def shortest_path(
        self,
        graph: KnowledgeGraph,
        start: str,
        target: str,
    ) -> list[str]:
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            current, path = queue.popleft()

            if current == target:
                return path

            if current in visited:
                continue

            visited.add(current)

            for edge in graph.edges:
                if edge.source == current:
                    queue.append((edge.target, path + [edge.target]))

        return []

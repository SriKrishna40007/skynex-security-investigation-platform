from collections import deque

from app.engines.graph.models import KnowledgeGraph


class GraphTraversal:
    """Breadth-first traversal over a KnowledgeGraph."""

    def reachable_nodes(
        self,
        graph: KnowledgeGraph,
        start_node: str,
    ) -> set[str]:
        visited: set[str] = set()
        queue = deque([start_node])

        while queue:
            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            for edge in graph.edges:
                if edge.source == current and edge.target not in visited:
                    queue.append(edge.target)

        return visited

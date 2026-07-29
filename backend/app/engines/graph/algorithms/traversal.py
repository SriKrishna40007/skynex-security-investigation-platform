from __future__ import annotations

from collections import deque

from app.engines.graph.models import KnowledgeGraph


class BreadthFirstTraversal:
    """
    Performs breadth-first traversal over a KnowledgeGraph.
    """

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

            for edge in graph.neighbors(current):
                if edge.target not in visited:
                    queue.append(edge.target)

        return order

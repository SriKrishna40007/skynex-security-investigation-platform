from __future__ import annotations

from collections import defaultdict

from app.application.graph.edge import GraphEdge
from app.application.graph.node import GraphNode


class KnowledgeGraph:
    """
    In-memory directed graph representing cloud infrastructure.

    Nodes represent resources.

    Edges represent relationships between resources.
    """

    def __init__(self) -> None:

        self._nodes: dict[str, GraphNode] = {}

        self._adjacency: dict[str, list[GraphEdge]] = defaultdict(list)

    def add_node(
        self,
        node: GraphNode,
    ) -> None:

        self._nodes[node.resource.id] = node

    def add_edge(
        self,
        source_id: str,
        edge: GraphEdge,
    ) -> None:

        self._adjacency[source_id].append(edge)

    def get_node(
        self,
        resource_id: str,
    ) -> GraphNode | None:

        return self._nodes.get(resource_id)

    def neighbors(
        self,
        resource_id: str,
    ) -> list[GraphEdge]:

        return self._adjacency.get(resource_id, [])

    @property
    def nodes(
        self,
    ) -> dict[str, GraphNode]:

        return self._nodes

    @property
    def adjacency(
        self,
    ) -> dict[str, list[GraphEdge]]:

        return self._adjacency

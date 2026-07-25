from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from app.engines.graph.models.edge import GraphEdge
from app.engines.graph.models.node import GraphNode


@dataclass(slots=True)
class KnowledgeGraph:
    """
    Represents the infrastructure as a directed graph.

    Nodes and edges preserve the original graph structure while the
    adjacency index enables efficient traversal algorithms.
    """

    nodes: list[GraphNode] = field(default_factory=list)

    edges: list[GraphEdge] = field(default_factory=list)

    adjacency: dict[str, list[GraphEdge]] = field(
        default_factory=lambda: defaultdict(list)
    )

    node_index: dict[str, GraphNode] = field(
        default_factory=dict
    )

    def add_node(
        self,
        node: GraphNode,
    ) -> None:

        self.nodes.append(node)
        self.node_index[node.id] = node

    def add_edge(
        self,
        edge: GraphEdge,
    ) -> None:

        self.edges.append(edge)
        self.adjacency[edge.source].append(edge)

    def neighbors(
        self,
        node_id: str,
    ) -> list[GraphEdge]:

        return self.adjacency.get(node_id, [])

    def get_node(
        self,
        node_id: str,
    ) -> GraphNode | None:

        return self.node_index.get(node_id)

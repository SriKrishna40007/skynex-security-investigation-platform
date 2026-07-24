from dataclasses import dataclass, field

from app.engines.graph.models.edge import GraphEdge
from app.engines.graph.models.node import GraphNode


@dataclass(slots=True)
class KnowledgeGraph:
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)

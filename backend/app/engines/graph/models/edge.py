from dataclasses import dataclass, field


@dataclass(slots=True)
class GraphEdge:
    source: str
    target: str
    relationship_type: str
    metadata: dict = field(default_factory=dict)

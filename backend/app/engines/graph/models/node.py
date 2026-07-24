from dataclasses import dataclass, field


@dataclass(slots=True)
class GraphNode:
    id: str
    label: str
    resource_type: str
    metadata: dict = field(default_factory=dict)

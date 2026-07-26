from dataclasses import dataclass, field


@dataclass(slots=True)
class AttackPath:
    """
    Represents a potential attack path through the infrastructure.
    """

    source: str
    target: str

    nodes: list[str] = field(default_factory=list)

    hop_count: int = 0

    risk: str = "LOW"

    description: str = ""

    exists: bool = False

from dataclasses import dataclass, field


@dataclass(slots=True)
class EngineMetrics:
    """
    Execution metadata produced by an investigation engine.
    """

    engine: str

    duration_ms: float = 0.0

    processed_items: int = 0

    metadata: dict[str, int | float | str] = field(
        default_factory=dict
    )

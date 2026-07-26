from dataclasses import dataclass, field


@dataclass(slots=True)
class RiskAssessment:
    """
    Represents the overall security risk for an investigation.
    """

    score: int = 0

    severity: str = "LOW"

    reasons: list[str] = field(default_factory=list)

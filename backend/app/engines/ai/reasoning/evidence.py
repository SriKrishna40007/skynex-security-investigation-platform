from dataclasses import dataclass, field


@dataclass(slots=True)
class InvestigationEvidence:
    """
    Structured evidence collected from security analysis.
    """

    findings: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    severity: str = "LOW"

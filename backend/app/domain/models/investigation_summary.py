from dataclasses import dataclass, field


@dataclass(slots=True)
class InvestigationSummary:
    """
    Human-readable investigation generated from
    structured security analysis.
    """

    executive_summary: str = ""

    technical_summary: str = ""

    key_findings: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    confidence: str = "HIGH"

from app.application.context import AnalysisContext
from app.domain.models import InvestigationSummary
from app.engines.ai.base import AIInvestigationEngine
from app.engines.ai.reasoning import ReasoningEngine


class DefaultAIInvestigationEngine(AIInvestigationEngine):
    """
    Produces a human-readable investigation from
    structured security analysis.
    """

    def __init__(self) -> None:
        self._reasoning = ReasoningEngine()

    def analyze(
        self,
        context: AnalysisContext,
    ) -> InvestigationSummary:
        evidence = self._reasoning.analyze(
            context,
        )

        executive_summary = (
            f"Overall investigation severity is "
            f"{evidence.severity}."
        )

        technical_summary = (
            "Security analysis identified "
            f"{len(evidence.findings)} findings "
            "requiring investigation."
        )

        return InvestigationSummary(
            executive_summary=executive_summary,
            technical_summary=technical_summary,
            key_findings=evidence.findings,
            recommendations=evidence.recommendations,
            confidence="HIGH",
        )

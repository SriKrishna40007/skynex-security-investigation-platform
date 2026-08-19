from app.application.context.analysis_context import AnalysisContext
from app.domain.models.investigation import Investigation
from app.engines.investigation.context.candidate_context_engine import (
    CandidateContextEngine,
)
from app.engines.investigation.impact.candidate_impact_engine import (
    CandidateImpactEngine,
)


class AnalysisContextBuilder:
    """
    Builds a strongly typed analysis context from an investigation.

    Candidate context and candidate impact are derived from the canonical
    investigation relationships and candidates at this boundary so
    downstream reasoning and presentation layers consume one stable model.
    """

    def __init__(self) -> None:
        self._candidate_context = CandidateContextEngine()
        self._candidate_impact = CandidateImpactEngine()

    def build(
        self,
        investigation: Investigation,
    ) -> AnalysisContext:
        candidate_context = [
            self._candidate_context.build(
                investigation,
                candidate,
            )
            for candidate in investigation.candidates
        ]

        candidate_impact = [
            self._candidate_impact.analyze(
                investigation,
                candidate,
            )
            for candidate in investigation.candidates
        ]

        return AnalysisContext(
            resources=investigation.resources,
            relationships=investigation.relationships,
            candidates=list(investigation.candidates),
            candidate_context=candidate_context,
            candidate_impact=candidate_impact,
            attack_path=investigation.analysis.get("attack_path"),
            blast_radius=investigation.analysis.get(
                "blast_radius",
                [],
            ),
            blast_radius_analysis=investigation.analysis.get(
                "blast_radius_analysis",
            ),
            risk=investigation.analysis.get("risk"),
        )

from app.application.context.analysis_context import AnalysisContext
from app.domain.models.investigation import Investigation


class AnalysisContextBuilder:
    """
    Builds a strongly typed analysis context from an
    investigation.
    """

    def build(
        self,
        investigation: Investigation,
    ) -> AnalysisContext:
        return AnalysisContext(
            resources=investigation.resources,
            relationships=investigation.relationships,
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

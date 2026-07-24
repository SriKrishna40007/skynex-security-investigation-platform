from app.domain.models.investigation import Investigation
from app.engines.attack_path.implementations import DefaultAttackPathEngine
from app.engines.blast_radius.implementations import DefaultBlastRadiusEngine
from app.engines.correlation.implementations import TerraformCorrelationEngine
from app.engines.graph.implementations import KnowledgeGraphEngine


class InvestigationPipeline:
    """Coordinates the investigation workflow."""

    def __init__(self) -> None:
        self._correlation = TerraformCorrelationEngine()
        self._graph = KnowledgeGraphEngine()
        self._attack_path = DefaultAttackPathEngine()
        self._blast_radius = DefaultBlastRadiusEngine()

    def run(
        self,
        investigation: Investigation,
        source: str,
        target: str,
    ) -> Investigation:
        investigation = self._correlation.correlate(investigation)
        investigation = self._graph.build(investigation)
        investigation = self._attack_path.analyze(
            investigation,
            source,
            target,
        )
        investigation = self._blast_radius.analyze(
            investigation,
            source,
        )

        return investigation

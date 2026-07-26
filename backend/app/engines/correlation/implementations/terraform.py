from __future__ import annotations

from app.application.metrics import ExecutionTimer, MetricsCollector
from app.domain.models import EngineMetrics
from app.domain.models.investigation import Investigation
from app.engines.correlation.base import CorrelationEngine
from app.engines.correlation.builders.terraform_relationship_builder import (
    TerraformRelationshipBuilder,
)


class TerraformCorrelationEngine(CorrelationEngine):
    """
    Correlates canonical Terraform resources by discovering
    relationships between them.
    """

    def __init__(self) -> None:
        self._relationship_builder = TerraformRelationshipBuilder()
        self._metrics = MetricsCollector()

    def correlate(
        self,
        investigation: Investigation,
    ) -> Investigation:
        timer = ExecutionTimer()

        relationships = self._relationship_builder.build(
            investigation.resources,
        )

        investigation.relationships = relationships

        self._metrics.record(
            investigation,
            EngineMetrics(
                engine="Correlation Engine",
                duration_ms=timer.elapsed_ms(),
                processed_items=len(investigation.resources),
                metadata={
                    "relationships": len(relationships),
                },
            ),
        )

        return investigation

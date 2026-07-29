from __future__ import annotations

from app.application.metrics import ExecutionTimer, MetricsCollector
from app.domain.models import EngineMetrics
from app.domain.models.investigation import Investigation
from app.engines.correlation.base import CorrelationEngine
from app.engines.correlation.builders.relationship_builder import (
    RelationshipBuilder,
)


class CanonicalCorrelationEngine(CorrelationEngine):
    """
    Discovers relationships between canonical SKYNEX resources.

    Provider-specific integrations are responsible for normalization.
    Correlation operates exclusively on canonical domain evidence.
    """

    def __init__(self) -> None:
        self._relationship_builder = RelationshipBuilder()
        self._metrics = MetricsCollector()

    def correlate(
        self,
        investigation: Investigation,
    ) -> Investigation:
        timer = ExecutionTimer()

        discovered = self._relationship_builder.build(
            investigation.resources,
        )

        existing = {
            (
                relationship.source_id,
                relationship.target_id,
                relationship.relationship_type,
            )
            for relationship in investigation.relationships
        }

        for relationship in discovered:
            key = (
                relationship.source_id,
                relationship.target_id,
                relationship.relationship_type,
            )

            if key not in existing:
                investigation.relationships.append(relationship)
                existing.add(key)

        self._metrics.record(
            investigation,
            EngineMetrics(
                engine="Canonical Correlation Engine",
                duration_ms=timer.elapsed_ms(),
                processed_items=len(investigation.resources),
                metadata={
                    "relationships": len(investigation.relationships),
                    "discovered_relationships": len(discovered),
                },
            ),
        )

        return investigation

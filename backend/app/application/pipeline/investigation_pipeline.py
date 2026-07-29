from __future__ import annotations

from app.domain.models.investigation import Investigation
from app.engines.attack_path.implementations import DefaultAttackPathEngine
from app.engines.blast_radius.implementations import DefaultBlastRadiusEngine
from app.engines.correlation.implementations.canonical import (
    CanonicalCorrelationEngine,
)
from app.engines.graph.implementations import KnowledgeGraphEngine
from app.engines.risk.implementations import DefaultRiskEngine


class InvestigationPipeline:
    """
    Coordinates topology-aware SKYNEX investigation processing.

    The pipeline executes graph-based security analysis only when the
    investigation contains enough topology information to justify it.

    Provider-specific evidence must already be normalized into the canonical
    Investigation domain before entering this pipeline.
    """

    def __init__(self) -> None:
        self._correlation = CanonicalCorrelationEngine()
        self._graph = KnowledgeGraphEngine()
        self._attack_path = DefaultAttackPathEngine()
        self._blast_radius = DefaultBlastRadiusEngine()
        self._risk = DefaultRiskEngine()

    def execute(
        self,
        investigation: Investigation,
        *,
        source: str | None = None,
        target: str | None = None,
        compromised_resource: str | None = None,
    ) -> Investigation:
        """
        Execute investigation engines when supported by available evidence.

        Terraform resources can expose references that allow SKYNEX to derive
        relationships and build a knowledge graph.

        IAM policy findings currently contain authorization-risk evidence but
        not identity/resource topology. IAM investigations therefore remain
        canonical without fabricating attack paths or blast-radius data.
        """

        if self._supports_relationship_discovery(investigation):
            investigation = self._correlation.correlate(investigation)

        if investigation.relationships:
            investigation = self._graph.build(investigation)

        if (
            "knowledge_graph" in investigation.analysis
            and source is not None
            and target is not None
        ):
            investigation = self._attack_path.analyze(
                investigation,
                source,
                target,
            )

        blast_radius_source = compromised_resource or source

        if (
            "knowledge_graph" in investigation.analysis
            and blast_radius_source is not None
        ):
            investigation = self._blast_radius.analyze(
                investigation,
                blast_radius_source,
            )

        if self._has_topology_analysis(investigation):
            investigation = self._risk.analyze(investigation)

        return investigation

    def run(
        self,
        investigation: Investigation,
        source: str,
        target: str,
    ) -> Investigation:
        """
        Backward-compatible entry point for the original pipeline contract.
        """

        return self.execute(
            investigation,
            source=source,
            target=target,
            compromised_resource=source,
        )

    @staticmethod
    def _supports_relationship_discovery(
        investigation: Investigation,
    ) -> bool:
        """
        Detect canonical relationship evidence without coupling correlation
        to the provider that produced the resource.
        """

        return any(
            bool(resource.metadata.get("references"))
            for resource in investigation.resources
        )

    @staticmethod
    def _has_topology_analysis(
        investigation: Investigation,
    ) -> bool:
        return (
            "attack_path" in investigation.analysis
            or "blast_radius" in investigation.analysis
        )

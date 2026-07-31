from __future__ import annotations

from app.application.context import AnalysisContextBuilder
from app.domain.models.investigation import Investigation
from app.engines.ai.reasoning import ReasoningEngine
from app.schemas.investigation import (
    AttackPathAnalysisResponse,
    BlastRadiusAnalysisResponse,
    BlastRadiusImpactResponse,
    InvestigationResponse,
    ReasoningResponse,
    RiskAssessmentResponse,
)


class InvestigationResponseMapper:
    """
    Maps canonical SKYNEX investigation state into the public API contract.

    The mapper isolates HTTP presentation models from internal domain and
    analysis implementations. Provider-specific evidence must already be
    normalized before reaching this boundary.
    """

    def __init__(self) -> None:
        self._context_builder = AnalysisContextBuilder()
        self._reasoning = ReasoningEngine()

    def map(
        self,
        investigation: Investigation,
    ) -> InvestigationResponse:
        context = self._context_builder.build(investigation)
        reasoning = self._reasoning.analyze(context)

        attack_path = context.attack_path
        blast_radius_analysis = context.blast_radius_analysis
        risk = context.risk

        legacy_attack_path: list[str] = []

        if attack_path is not None and attack_path.exists:
            legacy_attack_path = list(attack_path.nodes)

        attack_path_response = None

        if attack_path is not None:
            attack_path_response = AttackPathAnalysisResponse(
                source=attack_path.source,
                target=attack_path.target,
                nodes=list(attack_path.nodes),
                hop_count=attack_path.hop_count,
                risk=attack_path.risk,
                description=attack_path.description,
                exists=attack_path.exists,
            )

        blast_radius_response = None

        if blast_radius_analysis is not None:
            blast_radius_response = BlastRadiusAnalysisResponse(
                compromised_resource=(blast_radius_analysis.compromised_resource),
                reachable_resources=list(blast_radius_analysis.reachable_resources),
                affected_resource_count=(blast_radius_analysis.affected_resource_count),
                maximum_depth=blast_radius_analysis.maximum_depth,
                impacts=[
                    BlastRadiusImpactResponse(
                        resource_id=impact.resource_id,
                        depth=impact.depth,
                        relationship_types=list(impact.relationship_types),
                    )
                    for impact in blast_radius_analysis.impacts
                ],
            )

        risk_response = None

        if risk is not None:
            risk_response = RiskAssessmentResponse(
                score=risk.score,
                severity=risk.severity,
                reasons=list(risk.reasons),
            )

        reasoning_response = ReasoningResponse(
            findings=list(reasoning.findings),
            recommendations=list(reasoning.recommendations),
            severity=reasoning.severity,
        )

        return InvestigationResponse(
            attack_path=legacy_attack_path,
            blast_radius=list(context.blast_radius),
            risk_score=investigation.risk_score,
            summary=investigation.summary,
            attack_path_analysis=attack_path_response,
            blast_radius_analysis=blast_radius_response,
            risk=risk_response,
            reasoning=reasoning_response,
        )

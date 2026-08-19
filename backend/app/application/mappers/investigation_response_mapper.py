from __future__ import annotations

from app.application.context import AnalysisContextBuilder
from app.domain.models.investigation import Investigation
from app.engines.ai.reasoning import ReasoningEngine
from app.engines.remediation import RemediationEngine
from app.schemas.investigation import (
    AttackPathAnalysisResponse,
    BlastRadiusAnalysisResponse,
    BlastRadiusImpactResponse,
    CandidateContextResponse,
    CandidateImpactAnalysisResponse,
    CandidateImpactResponse,
    CandidateRelatedResourceResponse,
    InvestigationCandidateResponse,
    InvestigationResponse,
    ReasoningResponse,
    RemediationResponse,
    ResourceResponse,
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
        self._remediation = RemediationEngine()

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

        remediation_responses = [
            RemediationResponse(
                finding_id=plan.finding_id,
                title=plan.title,
                severity=plan.severity,
                resource_id=plan.resource_id,
                steps=list(plan.steps),
                executable=plan.executable,
            )
            for finding in investigation.findings
            for plan in [self._remediation.generate(finding)]
        ]

        candidate_responses = [
            InvestigationCandidateResponse(
                resource_id=candidate.resource_id,
                candidate_type=str(candidate.candidate_type),
                reason=candidate.reason,
                evidence=list(candidate.evidence),
                confidence=candidate.confidence,
            )
            for candidate in investigation.candidates
        ]

        candidate_context_responses = [
            CandidateContextResponse(
                candidate_resource_id=item.candidate_resource_id,
                related_resources=[
                    CandidateRelatedResourceResponse(
                        resource_id=related.resource_id,
                        relationship_type=related.relationship_type,
                        direction=related.direction,
                        evidence=related.evidence,
                    )
                    for related in item.related_resources
                ],
                explanation=item.explanation,
            )
            for item in context.candidate_context
        ]

        resource_responses = [
            ResourceResponse(
                id=resource.id,
                name=resource.name,
                type=resource.type,
                provider=resource.provider,
                tags=dict(resource.tags),
                metadata=dict(resource.metadata),
            )
            for resource in investigation.resources
        ]

        candidate_impact_responses = [
            CandidateImpactAnalysisResponse(
                candidate_resource_id=item.candidate_resource_id,
                affected_resource_count=item.affected_resource_count,
                impacts=[
                    CandidateImpactResponse(
                        resource_id=impact.resource_id,
                        relationship_type=impact.relationship_type,
                        direction=impact.direction,
                        reason=impact.reason,
                        evidence=list(impact.evidence),
                    )
                    for impact in item.impacts
                ],
            )
            for item in context.candidate_impact
        ]

        return InvestigationResponse(
            resources=resource_responses,
            candidates=candidate_responses,
            candidate_context=candidate_context_responses,
            candidate_impact=candidate_impact_responses,
            attack_path=legacy_attack_path,
            blast_radius=list(context.blast_radius),
            risk_score=investigation.risk_score,
            summary=investigation.summary,
            attack_path_analysis=attack_path_response,
            blast_radius_analysis=blast_radius_response,
            risk=risk_response,
            reasoning=reasoning_response,
            remediations=remediation_responses,
        )

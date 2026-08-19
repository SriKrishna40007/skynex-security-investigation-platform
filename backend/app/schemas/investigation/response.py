from pydantic import BaseModel, Field

from app.schemas.investigation.candidate import InvestigationCandidateResponse
from app.schemas.investigation.candidate_context import CandidateContextResponse
from app.schemas.investigation.candidate_impact import CandidateImpactAnalysisResponse
from app.schemas.investigation.remediation_response import RemediationResponse
from .resource_response import ResourceResponse

class AttackPathAnalysisResponse(BaseModel):
    """
    Public representation of semantic attack-path analysis.

    The API contract intentionally exposes security meaning without leaking
    internal SKYNEX domain implementations.
    """

    source: str
    target: str
    nodes: list[str] = Field(default_factory=list)
    hop_count: int = 0
    risk: str = "LOW"
    description: str = ""
    exists: bool = False


class BlastRadiusImpactResponse(BaseModel):
    """
    Public evidence describing how compromise reaches one resource.
    """

    resource_id: str
    depth: int
    relationship_types: list[str] = Field(default_factory=list)


class BlastRadiusAnalysisResponse(BaseModel):
    """
    Public representation of evidence-aware compromise propagation.
    """

    compromised_resource: str
    reachable_resources: list[str] = Field(default_factory=list)
    affected_resource_count: int = 0
    maximum_depth: int = 0
    impacts: list[BlastRadiusImpactResponse] = Field(default_factory=list)


class RiskAssessmentResponse(BaseModel):
    """
    Public representation of canonical SKYNEX topology risk.
    """

    score: int = 0
    severity: str = "LOW"
    reasons: list[str] = Field(default_factory=list)


class ReasoningResponse(BaseModel):
    """
    Security reasoning intended for investigators and presentation layers.
    """

    findings: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    severity: str = "LOW"


class InvestigationResponse(BaseModel):
    """
    Stable public contract for a SKYNEX investigation.
    """

    id: str | None = None

    attack_path: list[str] = Field(default_factory=list)
    candidates: list[InvestigationCandidateResponse] = Field(
        default_factory=list,
    )

    candidate_context: list[CandidateContextResponse] = Field(
        default_factory=list,
    )

    candidate_impact: list[CandidateImpactAnalysisResponse] = Field(
        default_factory=list,
    )
    blast_radius: list[str] = Field(default_factory=list)
    risk_score: float = 0.0
    summary: str = ""
    resources: list[ResourceResponse] = Field(default_factory=list)
    attack_path_analysis: AttackPathAnalysisResponse | None = None
    blast_radius_analysis: BlastRadiusAnalysisResponse | None = None
    risk: RiskAssessmentResponse | None = None
    reasoning: ReasoningResponse | None = None

    remediations: list[RemediationResponse] = Field(
        default_factory=list,
    )

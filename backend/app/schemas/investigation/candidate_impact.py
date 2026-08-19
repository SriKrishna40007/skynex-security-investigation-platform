from pydantic import BaseModel, Field


class CandidateImpactResponse(BaseModel):
    """Public evidence describing direct candidate impact."""

    resource_id: str
    relationship_type: str
    direction: str
    reason: str
    evidence: list[str] = Field(default_factory=list)


class CandidateImpactAnalysisResponse(BaseModel):
    """Public impact analysis for an investigation candidate."""

    candidate_resource_id: str
    affected_resource_count: int = 0
    impacts: list[CandidateImpactResponse] = Field(
        default_factory=list,
    )

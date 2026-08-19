from pydantic import BaseModel, Field


class InvestigationCandidateResponse(BaseModel):
    """Public representation of a SKYNEX investigation candidate."""

    resource_id: str
    candidate_type: str
    reason: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = 0.0

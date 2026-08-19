from pydantic import BaseModel, Field


class CandidateRelatedResourceResponse(BaseModel):
    """Public relationship evidence surrounding an investigation candidate."""

    resource_id: str
    relationship_type: str
    direction: str
    evidence: str


class CandidateContextResponse(BaseModel):
    """Public infrastructure context for an investigation candidate."""

    candidate_resource_id: str
    related_resources: list[CandidateRelatedResourceResponse] = Field(
        default_factory=list,
    )
    explanation: str = ""

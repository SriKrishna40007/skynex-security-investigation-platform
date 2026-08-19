from pydantic import BaseModel, Field


class RemediationResponse(BaseModel):
    """
    Public representation of V1 remediation guidance.

    V1 provides guidance only and does not execute infrastructure changes.
    """

    finding_id: str
    title: str
    severity: str
    resource_id: str
    steps: list[str] = Field(default_factory=list)
    executable: bool = False

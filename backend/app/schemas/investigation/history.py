from datetime import datetime

from pydantic import BaseModel


class InvestigationHistoryResponse(BaseModel):
    """
    Lightweight response returned by the investigation history API.

    This intentionally exposes only summary information.
    Clients must use the investigation read endpoint to obtain
    the full investigation.
    """

    id: str

    investigation_type: str

    status: str

    severity: str

    risk_score: float

    summary: str

    created_at: datetime

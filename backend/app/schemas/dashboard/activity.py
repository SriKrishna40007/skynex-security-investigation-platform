from datetime import datetime

from pydantic import BaseModel


class DashboardActivityResponse(BaseModel):
    """
    Lightweight activity item displayed on the dashboard.
    """

    id: str

    investigation_type: str

    status: str

    severity: str

    summary: str

    risk_score: float

    created_at: datetime

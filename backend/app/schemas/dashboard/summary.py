from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    """
    Executive dashboard metrics displayed after authentication.
    """

    total_investigations: int = 0

    completed: int = 0

    failed: int = 0

    critical: int = 0

    high: int = 0

    medium: int = 0

    low: int = 0

    average_risk_score: float = 0.0

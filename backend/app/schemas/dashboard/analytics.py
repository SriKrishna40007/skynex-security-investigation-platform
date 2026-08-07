from pydantic import BaseModel, Field


class TrendPoint(BaseModel):
    label: str
    value: int


class SeverityDistribution(BaseModel):
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0


class InvestigationTypeDistribution(BaseModel):
    terraform: int = 0
    iam: int = 0


class DashboardAnalyticsResponse(BaseModel):
    """
    Dashboard analytics used by charts and widgets.
    """

    investigation_trend: list[TrendPoint] = Field(default_factory=list)

    average_risk_trend: list[TrendPoint] = Field(default_factory=list)

    severity_distribution: SeverityDistribution

    investigation_type_distribution: InvestigationTypeDistribution

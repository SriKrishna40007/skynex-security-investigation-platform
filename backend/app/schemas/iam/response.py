from pydantic import BaseModel


class ScanResponse(BaseModel):
    overall_risk_score: int
    findings: int
    recommendations: list[str]

from pydantic import BaseModel


class InvestigationResponse(BaseModel):
    attack_path: list[str]
    blast_radius: list[str]
    risk_score: float
    summary: str

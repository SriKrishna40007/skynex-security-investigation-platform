from pydantic import BaseModel


class InvestigationRequest(BaseModel):
    source: str
    target: str

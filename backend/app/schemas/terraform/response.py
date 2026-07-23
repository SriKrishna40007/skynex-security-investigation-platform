from pydantic import BaseModel


class ScanResponse(BaseModel):
    security_score: int
    findings: int

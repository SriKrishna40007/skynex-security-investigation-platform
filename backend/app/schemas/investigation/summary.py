"""
Purpose:
    Summary of an investigation.
"""

from pydantic import BaseModel


class Summary(BaseModel):
    """
    Investigation summary.
    """

    scanner: str

    security_score: int

    total_findings: int

    high: int

    medium: int

    low: int

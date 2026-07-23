"""
Purpose:
    Represents the calculated security risk.

Responsibilities:
    - Store severity level.
    - Store numerical score.
    - Store impact.
    - Store likelihood.
"""

from pydantic import BaseModel


class Risk(BaseModel):
    """
    Risk assessment for a finding.
    """

    level: str
    score: int

    impact: str | None = None
    likelihood: str | None = None

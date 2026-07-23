"""
Purpose:
    Final investigation report returned by the Investigation Engine.
"""

from pydantic import BaseModel

from app.schemas.investigation.finding import Finding
from app.schemas.investigation.summary import Summary


class InvestigationReport(BaseModel):
    """
    Canonical investigation report.
    """

    summary: Summary

    findings: list[Finding]

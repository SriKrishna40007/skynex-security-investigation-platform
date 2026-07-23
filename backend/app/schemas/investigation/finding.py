"""
Purpose:
    Canonical finding model shared by every security scanner.
"""

from pydantic import BaseModel

from app.schemas.investigation.evidence import Evidence
from app.schemas.investigation.remediation import Remediation
from app.schemas.investigation.risk import Risk


class Finding(BaseModel):
    """
    Common security finding.
    """

    scanner: str

    rule_id: str

    title: str

    description: str

    severity: str

    resource: str

    evidence: Evidence

    risk: Risk

    remediation: Remediation | None = None

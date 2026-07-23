"""
Purpose:
    Represents remediation guidance for a finding.
"""

from pydantic import BaseModel


class Remediation(BaseModel):
    """
    Remediation instructions.
    """

    title: str
    steps: list[str]

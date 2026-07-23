"""
Purpose:
    Represents the technical evidence that triggered a security finding.

Responsibilities:
    - Store the affected resource.
    - Store the matched attribute.
    - Store the detected value.
    - Store source location information.
"""

from pydantic import BaseModel


class Evidence(BaseModel):
    """
    Technical evidence for a security finding.
    """

    resource: str
    attribute: str
    value: str

    file: str | None = None
    line: int | None = None
    code: str | None = None

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.models.finding import Finding
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource


@dataclass(slots=True)
class Investigation:
    """
    Represents the complete result of a security investigation.
    """

    id: str
    name: str

    resources: list[Resource] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    risk_score: float = 0.0

    summary: str = ""

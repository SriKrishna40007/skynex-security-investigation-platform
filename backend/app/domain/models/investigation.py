from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.models.finding import Finding
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.graph.models import KnowledgeGraph
from app.engines.investigation.models.candidate import InvestigationCandidate


@dataclass(slots=True)
class Investigation:
    """
    Represents a complete security investigation.
    """

    resources: list[Resource] = field(default_factory=list)

    relationships: list[Relationship] = field(default_factory=list)

    findings: list[Finding] = field(default_factory=list)

    candidates: list[InvestigationCandidate] = field(default_factory=list)

    analysis: dict[str, Any] = field(default_factory=dict)

    risk_score: float = 0.0

    summary: str = ""

    graph: KnowledgeGraph | None = None

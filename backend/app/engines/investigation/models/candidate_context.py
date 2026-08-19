from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CandidateRelatedResource:
    """A resource related to an investigation candidate."""

    resource_id: str
    relationship_type: str
    direction: str
    evidence: str


@dataclass(slots=True)
class CandidateContext:
    """Evidence-backed infrastructure context around a candidate."""

    candidate_resource_id: str
    related_resources: list[CandidateRelatedResource] = field(default_factory=list)
    explanation: str = ""

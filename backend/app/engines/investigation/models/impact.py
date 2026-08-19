from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CandidateImpact:
    """Security impact associated with one investigation candidate."""

    resource_id: str
    relationship_type: str
    direction: str
    reason: str
    evidence: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CandidateImpactAnalysis:
    """Evidence-backed impact assessment for an investigation candidate."""

    candidate_resource_id: str
    impacts: list[CandidateImpact] = field(default_factory=list)

    @property
    def affected_resource_count(self) -> int:
        return len(self.impacts)

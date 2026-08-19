from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class CandidateType(StrEnum):
    """Security investigation candidate classification."""

    ENTRY_POINT = "entry_point"
    HIGH_VALUE_TARGET = "high_value_target"
    COMPROMISE_ANCHOR = "compromise_anchor"


@dataclass(slots=True)
class InvestigationCandidate:
    """A resource identified as worthy of deeper investigation."""

    resource_id: str
    candidate_type: CandidateType
    reason: str
    evidence: list[str] = field(default_factory=list)
    confidence: float = 0.0

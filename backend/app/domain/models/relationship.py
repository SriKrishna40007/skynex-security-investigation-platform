from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Relationship:
    """
    Represents a relationship between two cloud resources.
    """

    source_id: str
    target_id: str
    relationship_type: str

    metadata: dict[str, Any] = field(default_factory=dict)

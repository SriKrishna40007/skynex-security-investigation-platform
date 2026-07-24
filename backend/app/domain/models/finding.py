from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Finding:
    """
    Represents a security finding identified during an investigation.
    """

    id: str
    title: str
    description: str
    severity: str

    resource_id: str

    recommendation: str

    metadata: dict[str, Any] = field(default_factory=dict)

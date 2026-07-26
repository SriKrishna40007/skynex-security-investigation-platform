from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Resource:
    """
    Canonical cloud resource used throughout SKYNEX platform.

    Every cloud provider integration (Terraform, IAM, Azure,
    Kubernetes, etc.) must normalize its resources into this model.
    """

    id: str
    name: str
    type: str
    provider: str

    tags: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

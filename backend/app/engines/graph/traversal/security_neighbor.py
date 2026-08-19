from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecurityNeighbor:
    """
    A security-relevant graph neighbor.

    The underlying canonical GraphEdge is never mutated. Direction describes
    how security propagation reached the neighbor.
    """

    resource_id: str
    relationship_type: str
    direction: str

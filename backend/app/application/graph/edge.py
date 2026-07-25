from __future__ import annotations

from dataclasses import dataclass

from app.domain.models.relationship import Relationship


@dataclass(slots=True)
class GraphEdge:
    """
    Represents a directed relationship between two graph nodes.
    """

    relationship: Relationship

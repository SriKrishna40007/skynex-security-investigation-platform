from __future__ import annotations

from dataclasses import dataclass

from app.domain.models.resource import Resource


@dataclass(slots=True)
class GraphNode:
    """
    Represents a resource in the investigation graph.
    """

    resource: Resource

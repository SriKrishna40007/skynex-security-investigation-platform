from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource


class RelationshipRule(ABC):
    """
    Base contract for discovering relationships between resources.
    """

    @abstractmethod
    def discover(
        self,
        resources: list[Resource],
    ) -> list[Relationship]:
        """
        Discover relationships from a collection of canonical resources.
        """
        raise NotImplementedError

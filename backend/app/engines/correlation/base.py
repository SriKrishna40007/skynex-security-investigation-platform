from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.models.investigation import Investigation


class CorrelationEngine(ABC):
    """
    Base interface for all correlation engines.

    A correlation engine enriches an Investigation by discovering
    relationships between resources.
    """

    @abstractmethod
    def correlate(self, investigation: Investigation) -> Investigation:
        """
        Discover relationships between resources and return the
        enriched investigation.
        """
        raise NotImplementedError

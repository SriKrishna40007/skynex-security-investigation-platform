from abc import ABC, abstractmethod

from app.domain.models.investigation import Investigation


class GraphEngine(ABC):
    """Base contract for graph construction engines."""

    @abstractmethod
    def build(self, investigation: Investigation) -> Investigation:
        """
        Build a graph representation from an investigation.

        Returns the enriched investigation.
        """
        raise NotImplementedError

from abc import ABC, abstractmethod

from app.domain.models.investigation import Investigation


class BlastRadiusEngine(ABC):
    """Base contract for blast radius analysis."""

    @abstractmethod
    def analyze(
        self,
        investigation: Investigation,
        compromised_resource: str,
    ) -> Investigation:
        raise NotImplementedError

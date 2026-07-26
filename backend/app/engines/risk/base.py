from abc import ABC, abstractmethod

from app.domain.models.investigation import Investigation


class RiskEngine(ABC):
    """Base contract for risk analysis."""

    @abstractmethod
    def analyze(
        self,
        investigation: Investigation,
    ) -> Investigation:
        raise NotImplementedError

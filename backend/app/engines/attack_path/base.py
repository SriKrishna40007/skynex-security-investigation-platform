from abc import ABC, abstractmethod

from app.domain.models.investigation import Investigation


class AttackPathEngine(ABC):
    """Base contract for attack path analysis."""

    @abstractmethod
    def analyze(
        self,
        investigation: Investigation,
        source: str,
        target: str,
    ) -> Investigation:
        raise NotImplementedError

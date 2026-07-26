from abc import ABC, abstractmethod

from app.domain.models.investigation import Investigation


class RiskRule(ABC):
    """
    Base contract for a risk evaluation rule.
    """

    @abstractmethod
    def evaluate(
        self,
        investigation: Investigation,
    ) -> tuple[int, list[str]]:
        """
        Returns:
            score contribution,
            explanatory reasons
        """
        raise NotImplementedError

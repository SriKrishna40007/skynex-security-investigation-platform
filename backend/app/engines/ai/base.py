from abc import ABC, abstractmethod

from app.application.context import AnalysisContext
from app.domain.models import InvestigationSummary


class AIInvestigationEngine(ABC):
    """
    Generates a human-readable investigation from
    structured analysis.
    """

    @abstractmethod
    def analyze(
        self,
        context: AnalysisContext,
    ) -> InvestigationSummary:
        raise NotImplementedError

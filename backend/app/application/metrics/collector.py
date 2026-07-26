from app.domain.models import EngineMetrics
from app.domain.models.investigation import Investigation


class MetricsCollector:
    """
    Stores execution metrics produced during an investigation.
    """

    def record(
        self,
        investigation: Investigation,
        metrics: EngineMetrics,
    ) -> None:
        if "metrics" not in investigation.analysis:
            investigation.analysis["metrics"] = []

        investigation.analysis["metrics"].append(metrics)

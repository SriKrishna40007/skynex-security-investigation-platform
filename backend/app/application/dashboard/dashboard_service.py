from app.repositories import DashboardRepository
from app.schemas.dashboard import DashboardSummaryResponse


class DashboardService:
    """
    Application service responsible for dashboard analytics.

    Repository performs aggregation.
    Service maps results into the public response contract.
    """

    def __init__(
        self,
        repository: DashboardRepository,
    ):
        self.repository = repository

    def summary(
        self,
    ) -> DashboardSummaryResponse:

        metrics = self.repository.summary()

        return DashboardSummaryResponse(
            **metrics,
        )

from app.repositories import DashboardRepository
from app.schemas.dashboard import (
    DashboardActivityResponse,
    DashboardSummaryResponse,
)


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

    def activity(
        self,
        limit: int = 10,
    ) -> list[DashboardActivityResponse]:
        """
        Returns recent dashboard activity.
        """

        records = self.repository.activity(limit)

        return [
            DashboardActivityResponse(
                id=record.id,
                investigation_type=record.investigation_type,
                status=record.status,
                severity=record.severity,
                summary=record.summary,
                risk_score=record.risk_score,
                created_at=record.created_at,
            )
            for record in records
        ]

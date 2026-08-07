from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import InvestigationRecord


class DashboardRepository:
    """
    Read-only analytics repository for dashboard metrics.

    Business logic belongs in the service layer.
    This repository performs aggregation queries only.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def summary(self) -> dict[str, float | int]:

        statement = select(
            func.count().label("total"),
            func.sum(
                case(
                    (
                        InvestigationRecord.status == "completed",
                        1,
                    ),
                    else_=0,
                )
            ).label("completed"),
            func.sum(
                case(
                    (
                        InvestigationRecord.status == "failed",
                        1,
                    ),
                    else_=0,
                )
            ).label("failed"),
            func.sum(
                case(
                    (
                        InvestigationRecord.severity == "CRITICAL",
                        1,
                    ),
                    else_=0,
                )
            ).label("critical"),
            func.sum(
                case(
                    (
                        InvestigationRecord.severity == "HIGH",
                        1,
                    ),
                    else_=0,
                )
            ).label("high"),
            func.sum(
                case(
                    (
                        InvestigationRecord.severity == "MEDIUM",
                        1,
                    ),
                    else_=0,
                )
            ).label("medium"),
            func.sum(
                case(
                    (
                        InvestigationRecord.severity == "LOW",
                        1,
                    ),
                    else_=0,
                )
            ).label("low"),
            func.avg(InvestigationRecord.risk_score).label("average_risk_score"),
        )

        row = self.db.execute(statement).one()

        return {
            "total_investigations": row.total or 0,
            "completed": row.completed or 0,
            "failed": row.failed or 0,
            "critical": row.critical or 0,
            "high": row.high or 0,
            "medium": row.medium or 0,
            "low": row.low or 0,
            "average_risk_score": float(row.average_risk_score or 0),
        }

    def activity(
        self,
        limit: int = 10,
    ) -> list[InvestigationRecord]:
        """
        Returns the most recent investigations for the dashboard
        activity feed.
        """

        statement = (
            select(InvestigationRecord)
            .order_by(
                InvestigationRecord.created_at.desc(),
            )
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def analytics(
        self,
    ) -> dict:
        """
        Returns aggregated dashboard analytics using
        real database aggregations.
        """

        summary = self.summary()

        type_statement = select(
            InvestigationRecord.investigation_type,
            func.count().label("count"),
        ).group_by(
            InvestigationRecord.investigation_type,
        )

        type_distribution = {
            "terraform": 0,
            "iam": 0,
        }

        for investigation_type, count in self.db.execute(type_statement):
            if investigation_type in type_distribution:
                type_distribution[investigation_type] = count

        return {
            "investigation_trend": [],
            "average_risk_trend": [],
            "severity_distribution": {
                "critical": summary["critical"],
                "high": summary["high"],
                "medium": summary["medium"],
                "low": summary["low"],
            },
            "investigation_type_distribution": type_distribution,
        }

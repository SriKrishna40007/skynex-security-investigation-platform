from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.application.queries import InvestigationHistoryQuery
from app.models import InvestigationRecord


class InvestigationRepository:
    """
    Persistence boundary for owned SKYNEX investigations.

    Ownership filtering belongs here rather than in API endpoints or
    canonical security-analysis engines.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        owner_id: str,
        investigation_type: str,
        status: str,
        risk_score: float,
        severity: str,
        summary: str,
        result: dict[str, Any],
    ) -> InvestigationRecord:
        investigation = InvestigationRecord(
            owner_id=owner_id,
            investigation_type=investigation_type,
            status=status,
            risk_score=risk_score,
            severity=severity,
            summary=summary,
            result=result,
        )

        self.db.add(investigation)
        self.db.commit()
        self.db.refresh(investigation)

        return investigation

    def get_by_id(
        self,
        investigation_id: str,
    ) -> InvestigationRecord | None:
        statement = select(InvestigationRecord).where(
            InvestigationRecord.id == investigation_id
        )

        return self.db.scalar(statement)

    def get_owned_by_id(
        self,
        *,
        investigation_id: str,
        owner_id: str,
    ) -> InvestigationRecord | None:
        statement = select(InvestigationRecord).where(
            InvestigationRecord.id == investigation_id,
            InvestigationRecord.owner_id == owner_id,
        )

        return self.db.scalar(statement)

    def list_history(
        self,
        query: InvestigationHistoryQuery,
    ) -> list[InvestigationRecord]:

        offset = (query.page - 1) * query.size

        statement = select(InvestigationRecord).where(
            InvestigationRecord.owner_id == query.owner_id,
        )

        if query.status:
            statement = statement.where(
                InvestigationRecord.status == query.status,
            )

        if query.severity:
            statement = statement.where(
                InvestigationRecord.severity == query.severity,
            )

        if query.investigation_type:
            statement = statement.where(
                InvestigationRecord.investigation_type == query.investigation_type,
            )

        if query.search:
            statement = statement.where(
                InvestigationRecord.summary.ilike(f"%{query.search}%")
            )

        sortable_columns = {
            "created_at": InvestigationRecord.created_at,
            "risk_score": InvestigationRecord.risk_score,
            "severity": InvestigationRecord.severity,
        }

        sort_column = sortable_columns.get(
            query.sort_by,
            InvestigationRecord.created_at,
        )

        if query.descending:
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()

        statement = statement.order_by(sort_column).offset(offset).limit(query.size)

        return list(self.db.scalars(statement).all())

    def count(
        self,
        query: InvestigationHistoryQuery,
    ) -> int:
        """
        Returns the total number of investigations matching the
        current query before pagination.
        """

        statement = (
            select(func.count())
            .select_from(InvestigationRecord)
            .where(
                InvestigationRecord.owner_id == query.owner_id,
            )
        )

        if query.status:
            statement = statement.where(
                InvestigationRecord.status == query.status,
            )

        if query.severity:
            statement = statement.where(
                InvestigationRecord.severity == query.severity,
            )

        if query.investigation_type:
            statement = statement.where(
                InvestigationRecord.investigation_type == query.investigation_type,
            )

        if query.search:
            statement = statement.where(
                InvestigationRecord.summary.ilike(f"%{query.search}%")
            )

        return int(self.db.scalar(statement) or 0)

    def list_for_owner(
        self,
        owner_id: str,
    ) -> list[InvestigationRecord]:
        """
        Backward-compatible wrapper around the query-based API.

        Existing callers continue to use this method while newer
        collection endpoints can use InvestigationHistoryQuery directly.
        """

        return self.list_history(
            InvestigationHistoryQuery(
                owner_id=owner_id,
            )
        )

    def delete(
        self,
        owner_id: str,
        investigation_id: str,
    ) -> bool:
        """
        Deletes an investigation owned by the specified user.

        Returns True if deleted, otherwise False.
        """

        record = (
            self.db.query(InvestigationRecord)
            .filter(
                InvestigationRecord.id == investigation_id,
                InvestigationRecord.owner_id == owner_id,
            )
            .first()
        )

        if record is None:
            return False

        self.db.delete(record)
        self.db.commit()

        return True

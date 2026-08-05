from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

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

    def list_for_owner(
        self,
        owner_id: str,
    ) -> list[InvestigationRecord]:
        statement = (
            select(InvestigationRecord)
            .where(InvestigationRecord.owner_id == owner_id)
            .order_by(InvestigationRecord.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

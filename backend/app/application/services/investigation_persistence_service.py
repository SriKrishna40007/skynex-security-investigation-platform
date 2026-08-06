from app.application.queries import InvestigationHistoryQuery
from app.domain.models.investigation import Investigation
from app.models import InvestigationRecord
from app.repositories import InvestigationRepository
from app.schemas.investigation import InvestigationResponse


class InvestigationPersistenceService:
    """
    Application boundary responsible for persisting completed investigations.

    The canonical security-analysis domain remains persistence-neutral.
    Serialization into durable storage happens only after analysis has been
    mapped to the public investigation response contract.
    """

    def __init__(
        self,
        repository: InvestigationRepository,
    ) -> None:
        self._repository = repository

    def persist(
        self,
        *,
        owner_id: str,
        investigation_type: str,
        investigation: Investigation,
        response: InvestigationResponse,
    ) -> InvestigationRecord:
        severity = self._resolve_severity(response)

        return self._repository.create(
            owner_id=owner_id,
            investigation_type=investigation_type,
            status="completed",
            risk_score=investigation.risk_score,
            severity=severity,
            summary=investigation.summary,
            result=response.model_dump(mode="json"),
        )

    def history(
        self,
        owner_id: str,
        page: int = 1,
        size: int = 20,
        status: str | None = None,
        severity: str | None = None,
        investigation_type: str | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        descending: bool = True,
    ) -> list[InvestigationRecord]:
        """Return investigations owned by one authenticated user."""

        query = InvestigationHistoryQuery(
            owner_id=owner_id,
            page=page,
            size=size,
            status=status,
            severity=severity,
            investigation_type=investigation_type,
            search=search,
            sort_by=sort_by,
            descending=descending,
        )

        return self._repository.list_history(query)

    def read(
        self,
        *,
        owner_id: str,
        investigation_id: str,
    ) -> InvestigationRecord | None:
        """Return one investigation only if it belongs to the owner."""

        return self._repository.get_owned_by_id(
            investigation_id=investigation_id,
            owner_id=owner_id,
        )

    @staticmethod
    def _resolve_severity(
        response: InvestigationResponse,
    ) -> str:
        if response.risk is not None:
            return response.risk.severity

        if response.reasoning is not None:
            return response.reasoning.severity

        return "LOW"

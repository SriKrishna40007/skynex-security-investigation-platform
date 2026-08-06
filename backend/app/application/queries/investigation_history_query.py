from dataclasses import dataclass


@dataclass(slots=True)
class InvestigationHistoryQuery:
    """
    Query object describing investigation history retrieval.

    Pagination, filtering, sorting and searching belong here rather than
    expanding repository method signatures.
    """

    owner_id: str

    page: int = 1
    size: int = 20

    status: str | None = None
    severity: str | None = None
    investigation_type: str | None = None

    search: str | None = None

    sort_by: str = "created_at"
    descending: bool = True

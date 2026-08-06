from pydantic import BaseModel, Field

from .history import InvestigationHistoryResponse


class InvestigationHistoryCollectionResponse(BaseModel):
    """
    Paginated investigation history returned to authenticated users.
    """

    items: list[InvestigationHistoryResponse] = Field(default_factory=list)

    page: int

    size: int

    total: int

    pages: int

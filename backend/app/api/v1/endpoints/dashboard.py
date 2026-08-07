from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.dependencies.rbac import require_role
from app.application.dashboard import DashboardService
from app.core.database import get_db
from app.repositories import DashboardRepository
from app.schemas.dashboard import (
    DashboardActivityResponse,
    DashboardSummaryResponse,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            "admin",
            "investigator",
        )
    ),
) -> DashboardSummaryResponse:
    repository = DashboardRepository(db)

    service = DashboardService(repository)

    return service.summary()


@router.get(
    "/activity",
    response_model=list[DashboardActivityResponse],
)
def dashboard_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            "admin",
            "investigator",
        )
    ),
) -> list[DashboardActivityResponse]:
    repository = DashboardRepository(db)

    service = DashboardService(repository)

    return service.activity(limit)

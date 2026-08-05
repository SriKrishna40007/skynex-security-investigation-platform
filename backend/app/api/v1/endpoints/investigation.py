from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.v1.dependencies.rbac import require_role
from app.application.mappers import InvestigationResponseMapper
from app.application.orchestrators import InvestigationOrchestrator
from app.application.services import InvestigationPersistenceService
from app.core.database import get_db
from app.models.user import User
from app.repositories import InvestigationRepository
from app.schemas.investigation import (
    InvestigationHistoryResponse,
    InvestigationResponse,
)

router = APIRouter(
    prefix="/investigations",
    tags=["Investigations"],
)

orchestrator = InvestigationOrchestrator()
response_mapper = InvestigationResponseMapper()


@router.post(
    "/terraform",
    response_model=InvestigationResponse,
)
async def investigate_terraform(
    terraform_file: UploadFile = File(...),
    source: str = Form(...),
    target: str = Form(...),
    current_user: User = Depends(require_role("admin", "investigator")),
    db: Session = Depends(get_db),
) -> InvestigationResponse:

    result = await orchestrator.investigate_terraform(
        terraform_file=terraform_file,
        source=source,
        target=target,
    )

    response = response_mapper.map(result)

    repository = InvestigationRepository(db)
    persistence_service = InvestigationPersistenceService(repository)

    persistence_service.persist(
        owner_id=current_user.id,
        investigation_type="terraform",
        investigation=result,
        response=response,
    )

    return response


@router.get(
    "",
    response_model=list[InvestigationHistoryResponse],
)
def investigation_history(
    current_user: User = Depends(require_role("admin", "investigator")),
    db: Session = Depends(get_db),
) -> list[InvestigationHistoryResponse]:

    repository = InvestigationRepository(db)

    service = InvestigationPersistenceService(repository)

    records = service.history(current_user.id)

    return [
        InvestigationHistoryResponse(
            id=r.id,
            investigation_type=r.investigation_type,
            status=r.status,
            severity=r.severity,
            risk_score=r.risk_score,
            summary=r.summary,
            created_at=r.created_at,
        )
        for r in records
    ]


@router.get(
    "/{investigation_id}",
    response_model=InvestigationResponse,
)
def read_investigation(
    investigation_id: str,
    current_user: User = Depends(require_role("admin", "investigator")),
    db: Session = Depends(get_db),
) -> InvestigationResponse:

    repository = InvestigationRepository(db)
    service = InvestigationPersistenceService(repository)

    record = service.read(
        owner_id=current_user.id,
        investigation_id=investigation_id,
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found.",
        )

    return InvestigationResponse.model_validate(record.result)

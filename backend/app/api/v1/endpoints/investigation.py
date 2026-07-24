from fastapi import APIRouter, File, Form, UploadFile

from app.application.orchestrators import InvestigationOrchestrator
from app.schemas.investigation import InvestigationResponse

router = APIRouter(
    prefix="/investigations",
    tags=["Investigations"],
)

orchestrator = InvestigationOrchestrator()


@router.post(
    "/terraform",
    response_model=InvestigationResponse,
)
async def investigate_terraform(
    terraform_file: UploadFile = File(...),
    source: str = Form(...),
    target: str = Form(...),
) -> InvestigationResponse:

    result = await orchestrator.investigate_terraform(
        terraform_file=terraform_file,
        source=source,
        target=target,
    )

    return InvestigationResponse(
        attack_path=result.analysis.get("attack_path", []),
        blast_radius=sorted(
            result.analysis.get("blast_radius", set())
        ),
        risk_score=result.risk_score,
        summary=result.summary,
    )

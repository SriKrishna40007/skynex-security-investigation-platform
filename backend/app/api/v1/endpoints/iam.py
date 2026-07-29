from fastapi import APIRouter, Depends, File, UploadFile

from app.api.v1.dependencies.auth import get_current_user
from app.application.orchestrators import InvestigationOrchestrator
from app.models.user import User
from app.schemas.iam.response import ScanResponse

router = APIRouter(
    prefix="/scan",
    tags=["IAM"],
)

orchestrator = InvestigationOrchestrator()


@router.post(
    "/iam",
    response_model=ScanResponse,
)
async def scan_iam_policy(
    policy: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> ScanResponse:
    """
    Analyze an uploaded IAM policy through the canonical SKYNEX
    investigation architecture.
    """

    investigation = await orchestrator.investigate_iam_upload(policy)

    iam_analysis = investigation.analysis["iam"]

    return ScanResponse(
        overall_risk_score=int(iam_analysis["overall_risk_score"]),
        findings=int(iam_analysis["finding_count"]),
        recommendations=list(iam_analysis["recommendations"]),
    )

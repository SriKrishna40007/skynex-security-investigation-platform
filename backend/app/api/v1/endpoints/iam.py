from fastapi import APIRouter, File, UploadFile

from app.schemas.iam.response import ScanResponse
from app.services.scan_service import ScanService

router = APIRouter(
    prefix="/scan",
    tags=["IAM"],
)

scan_service = ScanService()


@router.post("/iam", response_model=ScanResponse)
async def scan_iam_policy(
    policy: UploadFile = File(...),
) -> ScanResponse:
    return await scan_service.scan_iam_policy(policy)

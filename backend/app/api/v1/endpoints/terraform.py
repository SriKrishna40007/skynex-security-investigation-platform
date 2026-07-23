from fastapi import APIRouter, File, UploadFile

from app.schemas.investigation import InvestigationResponse
from app.services.scan_service import ScanService

router = APIRouter(
    prefix="/scan",
    tags=["Terraform"],
)

scan_service = ScanService()


@router.post(
    "/terraform",
    response_model=InvestigationResponse,
)
async def scan_terraform_file(
    terraform_file: UploadFile = File(...),
) -> InvestigationResponse:
    return await scan_service.scan_terraform_file(terraform_file)
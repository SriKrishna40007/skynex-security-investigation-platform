from fastapi import APIRouter, File, UploadFile

from app.schemas.investigation import InvestigationReport
from app.services.scan_service import ScanService

router = APIRouter(
    prefix="/scan",
    tags=["Terraform"],
)

scan_service = ScanService()


@router.post(
    "/terraform",
    response_model=InvestigationReport,
)
async def scan_terraform_file(
    terraform_file: UploadFile = File(...),
) -> InvestigationReport:
    return await scan_service.scan_terraform_file(terraform_file)

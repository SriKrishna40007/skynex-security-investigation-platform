from fastapi import APIRouter, File, UploadFile

from app.schemas.terraform.response import ScanResponse
from app.services.scan_service import ScanService

router = APIRouter(
    prefix="/scan",
    tags=["Terraform"],
)

scan_service = ScanService()


@router.post("/terraform", response_model=ScanResponse)
async def scan_terraform_file(
    terraform_file: UploadFile = File(...),
) -> ScanResponse:
    return await scan_service.scan_terraform_file(terraform_file)

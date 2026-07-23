from fastapi import UploadFile

from app.integrations.iam.adapter import IAMEngineAdapter
from app.integrations.terraform.adapter import TerraformScannerAdapter

from app.schemas.iam.response import ScanResponse as IAMScanResponse
from app.schemas.terraform.response import (
    ScanResponse as TerraformScanResponse,
)


class ScanService:
    """Coordinates security scan workflows."""

    def __init__(self) -> None:
        self.iam_adapter = IAMEngineAdapter()
        self.terraform_adapter = TerraformScannerAdapter()

    async def scan_iam_policy(
        self,
        policy: UploadFile,
    ) -> IAMScanResponse:
        return await self.iam_adapter.analyze(policy)

    async def scan_terraform_file(
        self,
        terraform_file: UploadFile,
    ) -> TerraformScanResponse:
        return await self.terraform_adapter.analyze(
            terraform_file
        )
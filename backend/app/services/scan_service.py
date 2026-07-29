from fastapi import UploadFile

from app.integrations.terraform.adapter import TerraformScannerAdapter
from app.services.investigation_service import InvestigationService


class ScanService:
    """
    Legacy Terraform scan service.

    IAM investigation orchestration is handled by
    InvestigationOrchestrator through the canonical SKYNEX domain.
    """

    def __init__(self) -> None:
        self.terraform_adapter = TerraformScannerAdapter()
        self.investigation_service = InvestigationService()

    async def scan_terraform_file(
        self,
        terraform_file: UploadFile,
    ):
        result = await self.terraform_adapter.scan(terraform_file)

        return self.investigation_service.build_terraform_report(result)

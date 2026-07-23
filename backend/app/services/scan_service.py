from app.integrations.iam.adapter import IAMEngineAdapter
from app.integrations.terraform.adapter import TerraformScannerAdapter
from app.services.investigation_service import InvestigationService


class ScanService:
    def __init__(self):
        self.iam_adapter = IAMEngineAdapter()
        self.terraform_adapter = TerraformScannerAdapter()
        self.investigation_service = InvestigationService()

    def scan_iam_policy(self, policy: dict):
        result = self.iam_adapter.scan(policy)
        return self.investigation_service.build_iam_report(result)

    async def scan_terraform_file(self, terraform_file):
        result = await self.terraform_adapter.scan(terraform_file)
        return self.investigation_service.build_terraform_report(result)
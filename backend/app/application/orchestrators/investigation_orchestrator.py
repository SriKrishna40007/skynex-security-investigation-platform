from fastapi import UploadFile

from app.application.builders import InvestigationBuilder
from app.application.pipeline import InvestigationPipeline
from app.integrations.terraform import TerraformScannerAdapter


class InvestigationOrchestrator:
    """
    Coordinates the complete investigation workflow.
    """

    def __init__(self) -> None:
        self.adapter = TerraformScannerAdapter()
        self.builder = InvestigationBuilder()
        self.pipeline = InvestigationPipeline()

    async def investigate_terraform(
        self,
        terraform_file: UploadFile,
        source: str,
        target: str,
    ):
        scan_result = await self.adapter.scan(terraform_file)

        investigation = self.builder.from_terraform_scan(scan_result)

        return self.pipeline.run(
            investigation=investigation,
            source=source,
            target=target,
        )

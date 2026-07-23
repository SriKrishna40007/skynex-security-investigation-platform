from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from app.schemas.terraform.response import ScanResponse

from terraform_security_analyzer import TerraformScanner


class TerraformScannerAdapter:
    """
    Adapter between the Security Investigation Workspace and the
    Terraform Security Analyzer SDK.
    """

    def __init__(self) -> None:
        self.scanner = TerraformScanner()

    async def analyze(
        self,
        terraform_file: UploadFile,
    ) -> ScanResponse:

        file_content = await terraform_file.read()

        with NamedTemporaryFile(
            delete=False,
            suffix=".tf",
        ) as temp_file:

            temp_file.write(file_content)

            temp_path = Path(temp_file.name)

        result = self.scanner.scan(temp_path)

        return ScanResponse(
            security_score=result["security_score"],
            findings=len(result["findings"]),
        )

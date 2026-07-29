from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from terraform_security_analyzer import TerraformScanner


class TerraformScannerAdapter:
    """
    Adapter between the Security Investigation Workspace
    and the Terraform Security Analyzer SDK.
    """

    def __init__(self) -> None:
        self.scanner = TerraformScanner()

    async def scan(self, terraform_file: UploadFile) -> dict:
        """
        Scan a Terraform configuration and return the raw SDK result.
        """

        file_content = await terraform_file.read()

        with NamedTemporaryFile(
            delete=False,
            suffix=".tf",
        ) as temp_file:
            temp_file.write(file_content)
            temp_path = Path(temp_file.name)

        return self.scanner.scan(temp_path)

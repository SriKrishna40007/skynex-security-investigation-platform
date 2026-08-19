from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile
from terraform_security_analyzer import TerraformScanner

from app.integrations.terraform.exceptions import TerraformValidationError


class TerraformScannerAdapter:
    """
    Adapter between the Security Investigation Workspace
    and the Terraform Security Analyzer SDK.

    The adapter owns transport/integration validation and normalizes
    Terraform resource identity into the canonical SKYNEX model.
    """

    def __init__(self) -> None:
        self.scanner = TerraformScanner()

    async def scan(self, terraform_file: UploadFile) -> dict:
        """
        Scan a Terraform configuration and return the normalized SDK result.

        SDK parsing failures are converted into TerraformValidationError.

        Terraform resources using `count` are expanded into distinct
        canonical resource instances so downstream SKYNEX graph analysis
        can reason about each instance independently.
        """

        file_content = await terraform_file.read()

        with NamedTemporaryFile(
            delete=False,
            suffix=".tf",
        ) as temp_file:
            temp_file.write(file_content)
            temp_path = Path(temp_file.name)

        try:
            try:
                result = self.scanner.scan(temp_path)
            except (ValueError, TypeError, KeyError) as exc:
                raise TerraformValidationError(
                    "Invalid Terraform configuration."
                ) from exc

            self._validate_unique_resource_addresses(result)
            self._expand_count_resources(result)
            self._validate_unique_resource_addresses(result)

            return result

        finally:
            temp_path.unlink(missing_ok=True)

    @staticmethod
    def _validate_unique_resource_addresses(
        scan_result: dict,
    ) -> None:
        resources = scan_result.get("resources", [])

        seen: set[str] = set()

        for resource in resources:
            resource_id = (
                f"{resource.resource_type}.{resource.resource_name}"
            )

            if resource_id in seen:
                raise TerraformValidationError(
                    f"Duplicate Terraform resource address: {resource_id}"
                )

            seen.add(resource_id)

    @staticmethod
    def _expand_count_resources(
        scan_result: dict,
    ) -> None:
        """
        Expand Terraform resources declaring an integer `count`.

        Example:

            aws_instance.fleet
                count = 10

        becomes:

            aws_instance.fleet[0]
            ...
            aws_instance.fleet[9]

        Resource attributes are copied independently so downstream
        canonicalization cannot accidentally mutate sibling instances.
        """

        resources = scan_result.get("resources", [])

        expanded = []

        for resource in resources:
            count = resource.attributes.get("count")

            if not isinstance(count, int) or isinstance(count, bool):
                expanded.append(resource)
                continue

            if count < 0:
                raise TerraformValidationError(
                    f"Invalid Terraform count for "
                    f"{resource.resource_type}.{resource.resource_name}: {count}"
                )

            for index in range(count):
                instance = deepcopy(resource)
                instance.resource_name = (
                    f"{resource.resource_name}[{index}]"
                )
                expanded.append(instance)

        scan_result["resources"] = expanded

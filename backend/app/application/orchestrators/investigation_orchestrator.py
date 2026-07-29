from __future__ import annotations

from typing import Any

from fastapi import UploadFile

from app.application.builders.investigation_builder import InvestigationBuilder
from app.application.pipeline.investigation_pipeline import InvestigationPipeline
from app.domain.models.investigation import Investigation
from app.integrations.iam.adapter import IAMEngineAdapter
from app.integrations.terraform.adapter import TerraformScannerAdapter


class InvestigationOrchestrator:
    """
    Application-level orchestration boundary for SKYNEX investigations.

    Provider-specific engine results are normalized into the canonical
    Investigation domain before downstream SKYNEX processing.
    """

    def __init__(self) -> None:
        self._terraform_adapter = TerraformScannerAdapter()
        self._iam_adapter = IAMEngineAdapter()
        self._builder = InvestigationBuilder()
        self._pipeline = InvestigationPipeline()

    async def investigate_terraform(
        self,
        terraform_file: UploadFile,
        *,
        source: str | None = None,
        target: str | None = None,
        compromised_resource: str | None = None,
    ) -> Investigation:
        """
        Execute the topology-aware Terraform investigation flow.
        """

        scan_result = await self._terraform_adapter.scan(terraform_file)

        investigation = self._builder.from_terraform_scan(scan_result)

        return self._pipeline.execute(
            investigation,
            source=source,
            target=target,
            compromised_resource=compromised_resource,
        )

    def investigate_iam_policy(
        self,
        policy_data: dict[str, Any],
    ) -> Investigation:
        """
        Analyze parsed IAM policy data and normalize the result into SKYNEX.
        """

        analysis_result = self._iam_adapter.analyze_policy(policy_data)

        return self._builder.from_iam_analysis(analysis_result)

    async def investigate_iam_upload(
        self,
        policy: UploadFile,
    ) -> Investigation:
        """
        Analyze an uploaded IAM policy and normalize the result into SKYNEX.
        """

        analysis_result = await self._iam_adapter.analyze_upload(policy)

        return self._builder.from_iam_analysis(analysis_result)

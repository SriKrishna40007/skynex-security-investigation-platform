from fastapi import UploadFile

from app.schemas.iam.response import ScanResponse


class ScanService:
    """Orchestrates security scan workflows."""

    async def scan_iam_policy(
        self,
        policy: UploadFile,
    ) -> ScanResponse:
        return ScanResponse(
            message=f"Received {policy.filename}"
        )
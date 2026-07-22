from fastapi import UploadFile

from app.schemas.iam.response import ScanResponse


class IAMEngineAdapter:
    """Adapter for communicating with the IAM Intelligence Engine."""

    async def analyze(
        self,
        policy: UploadFile,
    ) -> ScanResponse:
        return ScanResponse(
            message=f"IAM Engine analyzed {policy.filename}"
        )
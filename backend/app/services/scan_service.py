from fastapi import UploadFile

from app.integrations.iam.adapter import IAMEngineAdapter
from app.schemas.iam.response import ScanResponse


class ScanService:
    """Coordinates security scan workflows."""

    def __init__(self) -> None:
        self.iam_adapter = IAMEngineAdapter()

    async def scan_iam_policy(
        self,
        policy: UploadFile,
    ) -> ScanResponse:
        return await self.iam_adapter.analyze(policy)
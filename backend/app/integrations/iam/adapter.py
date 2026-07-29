import json

from fastapi import UploadFile

from app.schemas.iam.response import ScanResponse

from iam_intelligence_engine import IAMEngine
from iam_intelligence_engine.application.dto.analysis_request import AnalysisRequest


class IAMEngineAdapter:
    def __init__(self) -> None:
        self.engine = IAMEngine()

    async def analyze(self, policy: UploadFile) -> ScanResponse:
        policy_content = await policy.read()

        policy_dict = json.loads(policy_content.decode("utf-8"))

        request = AnalysisRequest(policy_data=policy_dict)

        result = self.engine.analyze(request)

        print(result)

        return ScanResponse(
            overall_risk_score=result.summary.overall_risk_score,
            findings=len(result.summary.findings),
            recommendations=result.summary.recommendations,
        )

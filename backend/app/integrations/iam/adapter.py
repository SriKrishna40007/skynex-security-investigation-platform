from __future__ import annotations

import json
from typing import Any

from fastapi import UploadFile

from iam_intelligence_engine import IAMEngine
from iam_intelligence_engine.application.dto.analysis_request import AnalysisRequest


class IAMEngineAdapter:
    """
    Adapter between SKYNEX and the IAM Intelligence Engine.

    Transport parsing belongs here. Engine results remain intact so the
    application layer can normalize them into the canonical SKYNEX domain.
    """

    def __init__(self) -> None:
        self.engine = IAMEngine()

    def analyze_policy(
        self,
        policy_data: dict[str, Any],
    ) -> Any:
        """Analyze an already parsed IAM policy."""

        request = AnalysisRequest(
            policy_data=policy_data,
        )

        return self.engine.analyze(request)

    async def analyze_upload(
        self,
        policy: UploadFile,
    ) -> Any:
        """Parse and analyze an uploaded IAM policy document."""

        policy_content = await policy.read()

        policy_dict = json.loads(policy_content.decode("utf-8"))

        return self.analyze_policy(policy_dict)

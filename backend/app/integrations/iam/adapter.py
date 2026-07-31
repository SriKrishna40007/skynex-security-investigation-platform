from __future__ import annotations

import json
from typing import Any

from fastapi import UploadFile

from iam_intelligence_engine import IAMEngine
from iam_intelligence_engine.application.dto.analysis_request import AnalysisRequest

from app.integrations.iam.contracts import IAMAnalysisEnvelope


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

        engine_policy = self._normalize_engine_policy(
            policy_data,
        )

        request = AnalysisRequest(
            policy_data=engine_policy,
        )

        return self.engine.analyze(request)

    @staticmethod
    def _normalize_engine_policy(
        policy_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Adapt valid IAM policy shapes to the IAM Intelligence Engine contract.

        The external engine currently expects Statement to be a list.
        SKYNEX preserves the original policy evidence and normalizes only
        the copy passed across the integration boundary.
        """

        engine_policy = dict(policy_data)

        statements = engine_policy.get("Statement", [])

        if isinstance(statements, dict):
            engine_policy["Statement"] = [statements]

        return engine_policy

    async def analyze_upload(
        self,
        policy: UploadFile,
    ) -> IAMAnalysisEnvelope:
        """
        Parse an uploaded IAM policy and preserve the analyzed evidence.
        """

        policy_content = await policy.read()

        policy_dict = json.loads(
            policy_content.decode("utf-8"),
        )

        analysis_result = self.analyze_policy(
            policy_dict,
        )

        return IAMAnalysisEnvelope(
            analysis_result=analysis_result,
            policy_data=policy_dict,
        )

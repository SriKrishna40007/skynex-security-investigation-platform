from __future__ import annotations

import json
from typing import Any

from fastapi import UploadFile

from iam_intelligence_engine import IAMEngine
from iam_intelligence_engine.application.dto.analysis_request import AnalysisRequest

from app.integrations.iam.contracts import IAMAnalysisEnvelope
from app.integrations.iam.exceptions import IAMPolicyValidationError


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
        """Analyze an already parsed and validated IAM policy."""

        engine_policy = self._normalize_engine_policy(policy_data)

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
        """

        engine_policy = dict(policy_data)

        statements = engine_policy.get("Statement", [])

        if isinstance(statements, dict):
            engine_policy["Statement"] = [statements]

        return engine_policy

    @staticmethod
    def _validate_policy(
        policy_data: Any,
    ) -> dict[str, Any]:
        if not isinstance(policy_data, dict):
            raise IAMPolicyValidationError(
                "IAM policy must be a JSON object."
            )

        missing = [
            key
            for key in ("Version", "Statement")
            if key not in policy_data
        ]

        if missing:
            raise IAMPolicyValidationError(
                f"IAM policy is missing required field(s): {', '.join(missing)}."
            )

        if not isinstance(policy_data["Version"], str):
            raise IAMPolicyValidationError(
                "IAM policy Version must be a string."
            )

        statements = policy_data["Statement"]

        if not isinstance(statements, (list, dict)):
            raise IAMPolicyValidationError(
                "IAM policy Statement must be an object or list."
            )

        return policy_data

    async def analyze_upload(
        self,
        policy: UploadFile,
    ) -> IAMAnalysisEnvelope:
        """
        Parse, validate, and analyze an uploaded IAM policy.
        """

        policy_content = await policy.read()

        try:
            policy_dict = json.loads(
                policy_content.decode("utf-8"),
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise IAMPolicyValidationError(
                "IAM policy must contain valid UTF-8 JSON."
            ) from exc

        policy_dict = self._validate_policy(policy_dict)

        analysis_result = self.analyze_policy(
            policy_dict,
        )

        return IAMAnalysisEnvelope(
            analysis_result=analysis_result,
            policy_data=policy_dict,
        )

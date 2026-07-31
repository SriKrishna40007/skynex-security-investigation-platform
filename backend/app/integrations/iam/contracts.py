from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class IAMAnalysisEnvelope:
    """
    Result returned by the IAM integration boundary.

    Preserves both the external engine result and the normalized policy
    evidence used to produce that result.
    """

    analysis_result: Any
    policy_data: dict[str, Any]

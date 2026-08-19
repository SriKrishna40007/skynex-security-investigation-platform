from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RemediationPlan:
    """
    Deterministic remediation guidance for a security finding.

    V1 produces guidance only. It does not execute infrastructure changes.
    """

    finding_id: str
    title: str
    severity: str
    resource_id: str
    steps: tuple[str, ...]
    executable: bool = False

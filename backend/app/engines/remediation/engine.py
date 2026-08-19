from __future__ import annotations

from app.domain.models.finding import Finding

from .models import RemediationPlan


class RemediationEngine:
    """
    Converts canonical security findings into deterministic remediation plans.

    The engine is intentionally execution-free in V1. It provides remediation
    guidance that can later be consumed by a controlled remediation workflow.
    """

    def generate(self, finding: Finding) -> RemediationPlan:
        steps = self._build_steps(finding)

        return RemediationPlan(
            finding_id=finding.id,
            title=finding.title,
            severity=finding.severity,
            resource_id=finding.resource_id,
            steps=tuple(steps),
        )

    @staticmethod
    def _build_steps(finding: Finding) -> list[str]:
        steps: list[str] = []

        if finding.recommendation.strip():
            steps.append(finding.recommendation.strip())

        if not steps:
            steps.append(
                "Review the affected resource and apply the least-privilege "
                "configuration appropriate for the finding."
            )

        steps.append(
            "Validate the change with the relevant security checks before deployment."
        )

        return steps

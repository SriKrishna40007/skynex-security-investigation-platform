from app.domain.models import RiskAssessment
from app.domain.models.investigation import Investigation
from app.engines.risk.base import RiskEngine
from app.engines.risk.rules import (
    AttackPathRule,
    BlastRadiusRule,
    RiskRule,
)


class DefaultRiskEngine(RiskEngine):
    """
    Aggregates all risk rules into a single assessment.
    """

    def __init__(self) -> None:
        self._rules: list[RiskRule] = [
            AttackPathRule(),
            BlastRadiusRule(),
        ]

    def analyze(
        self,
        investigation: Investigation,
    ) -> Investigation:
        score = 0
        reasons: list[str] = []

        for rule in self._rules:
            partial_score, partial_reasons = rule.evaluate(
                investigation,
            )

            score += partial_score
            reasons.extend(partial_reasons)

        score = min(score, 100)

        if score >= 80:
            severity = "CRITICAL"
        elif score >= 60:
            severity = "HIGH"
        elif score >= 30:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        investigation.analysis["risk"] = RiskAssessment(
            score=score,
            severity=severity,
            reasons=reasons,
        )

        return investigation

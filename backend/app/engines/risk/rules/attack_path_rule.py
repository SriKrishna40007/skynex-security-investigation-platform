from __future__ import annotations

from app.domain.models.investigation import Investigation

from .base import RiskRule


class AttackPathRule(RiskRule):
    """
    Scores investigation risk using semantic attack-path evidence.

    Attack-path discovery is responsible for determining the semantic
    significance of the path. This rule translates that established
    severity into an investigation-level score contribution.
    """

    _SEVERITY_SCORES = {
        "LOW": 10,
        "MEDIUM": 20,
        "HIGH": 30,
        "CRITICAL": 40,
    }

    def evaluate(
        self,
        investigation: Investigation,
    ) -> tuple[int, list[str]]:
        attack_path = investigation.analysis.get("attack_path")

        if attack_path is None:
            return 0, []

        if not attack_path.exists:
            return 0, []

        severity = attack_path.risk.upper()

        score = self._SEVERITY_SCORES.get(severity)

        if score is None:
            return (
                0,
                [
                    (
                        "Attack path exists but its semantic severity "
                        f"'{attack_path.risk}' is not recognized."
                    )
                ],
            )

        reasons = [
            (
                f"{severity} attack path exists from "
                f"{attack_path.source} to {attack_path.target}."
            )
        ]

        if attack_path.description:
            reasons.append(attack_path.description)

        return score, reasons

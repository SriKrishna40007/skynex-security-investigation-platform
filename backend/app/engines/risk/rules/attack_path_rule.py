from app.domain.models.investigation import Investigation

from .base import RiskRule


class AttackPathRule(RiskRule):
    """
    Scores risk based on attack path analysis.
    """

    def evaluate(
        self,
        investigation: Investigation,
    ) -> tuple[int, list[str]]:
        attack_path = investigation.analysis.get("attack_path")

        if attack_path is None:
            return 0, []

        if not attack_path.exists:
            return 0, []

        score = 30

        reasons = [
            (
                f"Attack path exists from "
                f"{attack_path.source} to {attack_path.target}."
            )
        ]

        if attack_path.hop_count >= 5:
            score += 20
            reasons.append(
                "Multiple lateral movement opportunities detected."
            )

        return score, reasons

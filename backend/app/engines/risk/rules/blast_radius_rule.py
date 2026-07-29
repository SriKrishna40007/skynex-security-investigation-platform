from app.domain.models.investigation import Investigation

from .base import RiskRule


class BlastRadiusRule(RiskRule):
    """
    Scores risk based on blast radius.
    """

    def evaluate(
        self,
        investigation: Investigation,
    ) -> tuple[int, list[str]]:
        blast_radius = investigation.analysis.get("blast_radius", [])

        affected = len(blast_radius)

        if affected <= 1:
            return 0, []

        score = min(affected * 5, 30)

        return score, [f"Compromise may affect {affected} connected resources."]

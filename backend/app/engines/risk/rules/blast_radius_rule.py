from __future__ import annotations

from app.domain.models.investigation import Investigation
from app.engines.blast_radius.models import BlastRadiusAnalysis

from .base import RiskRule


class BlastRadiusRule(RiskRule):
    """
    Scores risk from evidence-backed compromise propagation.

    Rich blast-radius analysis is preferred when available because it
    distinguishes the compromised resource from resources affected by
    propagation. The legacy blast-radius list remains supported for
    compatibility with older investigation producers.
    """

    def evaluate(
        self,
        investigation: Investigation,
    ) -> tuple[int, list[str]]:
        analysis = investigation.analysis.get("blast_radius_analysis")

        if isinstance(analysis, BlastRadiusAnalysis):
            return self._evaluate_rich_analysis(analysis)

        return self._evaluate_legacy_analysis(
            investigation.analysis.get(
                "blast_radius",
                [],
            )
        )

    def _evaluate_rich_analysis(
        self,
        analysis: BlastRadiusAnalysis,
    ) -> tuple[int, list[str]]:
        affected = analysis.affected_resource_count

        if affected == 0:
            return 0, []

        score = min(affected * 5, 30)

        reasons = [(f"Compromise may affect {affected} additional resources.")]

        if analysis.maximum_depth > 1:
            reasons.append(
                (f"Compromise propagation reaches depth {analysis.maximum_depth}.")
            )

        return score, reasons

    def _evaluate_legacy_analysis(
        self,
        blast_radius: list[str],
    ) -> tuple[int, list[str]]:
        affected = len(blast_radius)

        if affected <= 1:
            return 0, []

        score = min(affected * 5, 30)

        return (
            score,
            [
                (
                    "Legacy blast-radius evidence includes "
                    f"{affected} connected resources."
                )
            ],
        )

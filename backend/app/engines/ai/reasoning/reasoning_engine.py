from app.application.context import AnalysisContext

from .evidence import InvestigationEvidence


class ReasoningEngine:
    """
    Converts structured security analysis into investigation evidence.

    Reasoning operates exclusively on canonical SKYNEX analysis context.
    Provider-specific evidence must be normalized before reaching this layer.
    """

    def analyze(
        self,
        context: AnalysisContext,
    ) -> InvestigationEvidence:
        evidence = InvestigationEvidence()

        self._reason_about_attack_path(
            context,
            evidence,
        )

        self._reason_about_blast_radius(
            context,
            evidence,
        )

        self._reason_about_risk(
            context,
            evidence,
        )

        return evidence

    @staticmethod
    def _reason_about_attack_path(
        context: AnalysisContext,
        evidence: InvestigationEvidence,
    ) -> None:
        attack_path = context.attack_path

        if attack_path is None or not attack_path.exists:
            return

        evidence.findings.append(
            (
                "Attack path identified from "
                f"{attack_path.source} to {attack_path.target} "
                f"across {attack_path.hop_count} hop(s) "
                f"with {attack_path.risk.upper()} semantic risk."
            )
        )

        if attack_path.description:
            evidence.findings.append(attack_path.description)

        evidence.recommendations.append(
            "Investigate and break the highest-risk relationships "
            "along the attack path."
        )

    @staticmethod
    def _reason_about_blast_radius(
        context: AnalysisContext,
        evidence: InvestigationEvidence,
    ) -> None:
        analysis = context.blast_radius_analysis

        if analysis is None:
            affected = len(context.blast_radius)

            if affected:
                evidence.findings.append(f"Blast radius includes {affected} resources.")

                evidence.recommendations.append(
                    "Reduce lateral movement opportunities."
                )

            return

        affected = analysis.affected_resource_count

        if affected <= 0:
            return

        evidence.findings.append(
            (
                f"Compromise of {analysis.compromised_resource} "
                f"may affect {affected} additional resource(s) "
                f"across a maximum propagation depth of "
                f"{analysis.maximum_depth}."
            )
        )

        relationship_types = {
            relationship_type
            for impact in analysis.impacts
            for relationship_type in impact.relationship_types
        }

        if relationship_types:
            evidence.findings.append(
                (
                    "Observed propagation relationships: "
                    f"{', '.join(sorted(relationship_types))}."
                )
            )

        evidence.recommendations.append(
            "Reduce compromise propagation by restricting the "
            "relationships connecting affected resources."
        )

    @staticmethod
    def _reason_about_risk(
        context: AnalysisContext,
        evidence: InvestigationEvidence,
    ) -> None:
        risk = context.risk

        if risk is None:
            return

        evidence.severity = risk.severity

        evidence.findings.extend(risk.reasons)

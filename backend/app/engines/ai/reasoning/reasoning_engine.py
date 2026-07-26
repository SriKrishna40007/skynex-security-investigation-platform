from app.application.context import AnalysisContext

from .evidence import InvestigationEvidence


class ReasoningEngine:
    """
    Converts structured security analysis into
    investigation evidence.
    """

    def analyze(
        self,
        context: AnalysisContext,
    ) -> InvestigationEvidence:
        evidence = InvestigationEvidence()

        if context.attack_path and context.attack_path.exists:
            evidence.findings.append(
                (
                    f"Attack path identified from "
                    f"{context.attack_path.source} "
                    f"to {context.attack_path.target}."
                )
            )

            evidence.recommendations.append(
                "Investigate resources along the attack path."
            )

        affected = len(context.blast_radius)

        if affected:
            evidence.findings.append(
                f"Blast radius includes {affected} resources."
            )

            evidence.recommendations.append(
                "Reduce lateral movement opportunities."
            )

        if context.risk:
            evidence.severity = context.risk.severity

            evidence.findings.extend(
                context.risk.reasons
            )

        return evidence

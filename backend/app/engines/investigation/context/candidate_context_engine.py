from __future__ import annotations

from app.domain.models.investigation import Investigation
from app.engines.investigation.models.candidate import InvestigationCandidate
from app.engines.investigation.models.candidate_context import (
    CandidateContext,
    CandidateRelatedResource,
)


class CandidateContextEngine:
    """
    Build evidence-backed infrastructure context around an investigation
    candidate.

    Canonical relationships are preserved exactly as discovered. The engine
    only adds investigator-oriented direction metadata.
    """

    def build(
        self,
        investigation: Investigation,
        candidate: InvestigationCandidate,
    ) -> CandidateContext:
        related_resources: list[CandidateRelatedResource] = []

        resource_ids = {resource.id for resource in investigation.resources}

        for relationship in investigation.relationships:
            if relationship.source_id == candidate.resource_id:
                if relationship.target_id not in resource_ids:
                    continue

                related_resources.append(
                    CandidateRelatedResource(
                        resource_id=relationship.target_id,
                        relationship_type=relationship.relationship_type,
                        direction="outgoing",
                        evidence=(
                            f"{relationship.source_id} "
                            f"{relationship.relationship_type} "
                            f"{relationship.target_id}"
                        ),
                    )
                )

            elif relationship.target_id == candidate.resource_id:
                if relationship.source_id not in resource_ids:
                    continue

                related_resources.append(
                    CandidateRelatedResource(
                        resource_id=relationship.source_id,
                        relationship_type=relationship.relationship_type,
                        direction="incoming",
                        evidence=(
                            f"{relationship.source_id} "
                            f"{relationship.relationship_type} "
                            f"{relationship.target_id}"
                        ),
                    )
                )

        related_resources.sort(
            key=lambda item: (
                item.direction,
                item.resource_id,
                item.relationship_type,
            )
        )

        explanation = self._build_explanation(
            candidate,
            related_resources,
        )

        return CandidateContext(
            candidate_resource_id=candidate.resource_id,
            related_resources=related_resources,
            explanation=explanation,
        )

    @staticmethod
    def _build_explanation(
        candidate: InvestigationCandidate,
        related_resources: list[CandidateRelatedResource],
    ) -> str:
        if not related_resources:
            return (
                f"{candidate.resource_id} requires investigation, "
                "but no directly related infrastructure resources were "
                "identified from the available evidence."
            )

        incoming = [item for item in related_resources if item.direction == "incoming"]

        outgoing = [item for item in related_resources if item.direction == "outgoing"]

        parts = [
            (
                f"{candidate.resource_id} is an investigation candidate "
                f"because {candidate.reason.lower()}"
            )
        ]

        if incoming:
            incoming_resources = ", ".join(item.resource_id for item in incoming)
            parts.append(
                f"Related resources reference or depend on the candidate: "
                f"{incoming_resources}."
            )

        if outgoing:
            outgoing_resources = ", ".join(item.resource_id for item in outgoing)
            parts.append(f"The candidate has relationships to: {outgoing_resources}.")

        return " ".join(parts)

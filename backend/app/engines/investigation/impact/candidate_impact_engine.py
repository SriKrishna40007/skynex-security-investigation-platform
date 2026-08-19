from __future__ import annotations

from app.domain.models.investigation import Investigation
from app.engines.investigation.models.candidate import InvestigationCandidate
from app.engines.investigation.models.impact import (
    CandidateImpact,
    CandidateImpactAnalysis,
)


class CandidateImpactEngine:
    """
    Determine direct infrastructure impact for an investigation candidate.

    Candidate impact is intentionally different from blast radius.

    Blast radius answers:
        Where can security compromise propagate through directed edges?

    Candidate impact answers:
        Which resources directly depend on or reference this candidate?

    This engine therefore consumes canonical investigation relationships
    without changing their original direction or semantics.
    """

    def analyze(
        self,
        investigation: Investigation,
        candidate: InvestigationCandidate,
    ) -> CandidateImpactAnalysis:
        impacts: list[CandidateImpact] = []

        known_resource_ids = {resource.id for resource in investigation.resources}

        for relationship in investigation.relationships:
            if relationship.target_id != candidate.resource_id:
                continue

            if relationship.source_id not in known_resource_ids:
                continue

            impacts.append(
                CandidateImpact(
                    resource_id=relationship.source_id,
                    relationship_type=relationship.relationship_type,
                    direction="incoming",
                    reason=(
                        f"{relationship.source_id} depends on or references "
                        f"{candidate.resource_id}."
                    ),
                    evidence=[
                        (
                            f"{relationship.source_id} "
                            f"{relationship.relationship_type} "
                            f"{relationship.target_id}"
                        )
                    ],
                )
            )

        impacts.sort(
            key=lambda impact: (
                impact.resource_id,
                impact.relationship_type,
            )
        )

        return CandidateImpactAnalysis(
            candidate_resource_id=candidate.resource_id,
            impacts=impacts,
        )

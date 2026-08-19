from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.investigation.impact.candidate_impact_engine import (
    CandidateImpactEngine,
)
from app.engines.investigation.models.candidate import (
    CandidateType,
    InvestigationCandidate,
)


def test_identifies_resources_depending_on_candidate() -> None:
    investigation = Investigation(
        resources=[
            Resource(
                id="aws_instance.web",
                name="web",
                type="aws_instance",
                provider="terraform",
            ),
            Resource(
                id="aws_security_group.web",
                name="web",
                type="aws_security_group",
                provider="terraform",
            ),
            Resource(
                id="aws_vpc.production",
                name="production",
                type="aws_vpc",
                provider="terraform",
            ),
        ],
        relationships=[
            Relationship(
                source_id="aws_instance.web",
                target_id="aws_security_group.web",
                relationship_type="references",
            ),
            Relationship(
                source_id="aws_security_group.web",
                target_id="aws_vpc.production",
                relationship_type="belongs_to",
            ),
        ],
    )

    candidate = InvestigationCandidate(
        resource_id="aws_security_group.web",
        candidate_type=CandidateType.ENTRY_POINT,
        reason="Public ingress requires investigation.",
        evidence=["ingress_allows_0.0.0.0/0"],
        confidence=0.85,
    )

    analysis = CandidateImpactEngine().analyze(
        investigation,
        candidate,
    )

    assert analysis.candidate_resource_id == "aws_security_group.web"
    assert analysis.affected_resource_count == 1

    impact = analysis.impacts[0]

    assert impact.resource_id == "aws_instance.web"
    assert impact.relationship_type == "references"
    assert impact.direction == "incoming"
    assert "aws_instance.web references aws_security_group.web" in (impact.evidence)[0]


def test_does_not_treat_parent_context_as_direct_workload_impact() -> None:
    investigation = Investigation(
        resources=[
            Resource(
                id="aws_security_group.web",
                name="web",
                type="aws_security_group",
                provider="terraform",
            ),
            Resource(
                id="aws_vpc.production",
                name="production",
                type="aws_vpc",
                provider="terraform",
            ),
        ],
        relationships=[
            Relationship(
                source_id="aws_security_group.web",
                target_id="aws_vpc.production",
                relationship_type="belongs_to",
            ),
        ],
    )

    candidate = InvestigationCandidate(
        resource_id="aws_security_group.web",
        candidate_type=CandidateType.ENTRY_POINT,
        reason="Public ingress requires investigation.",
    )

    analysis = CandidateImpactEngine().analyze(
        investigation,
        candidate,
    )

    assert analysis.impacts == []
    assert analysis.affected_resource_count == 0

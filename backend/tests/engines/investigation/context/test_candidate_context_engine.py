from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.investigation.context.candidate_context_engine import (
    CandidateContextEngine,
)
from app.engines.investigation.models.candidate import (
    CandidateType,
    InvestigationCandidate,
)


def test_builds_incoming_and_outgoing_context() -> None:
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

    context = CandidateContextEngine().build(
        investigation,
        candidate,
    )

    assert context.candidate_resource_id == "aws_security_group.web"
    assert len(context.related_resources) == 2

    incoming = [
        item for item in context.related_resources if item.direction == "incoming"
    ]

    outgoing = [
        item for item in context.related_resources if item.direction == "outgoing"
    ]

    assert len(incoming) == 1
    assert incoming[0].resource_id == "aws_instance.web"
    assert incoming[0].relationship_type == "references"

    assert len(outgoing) == 1
    assert outgoing[0].resource_id == "aws_vpc.production"
    assert outgoing[0].relationship_type == "belongs_to"


def test_preserves_canonical_relationship_direction() -> None:
    investigation = Investigation(
        resources=[
            Resource(
                id="resource.a",
                name="a",
                type="test",
                provider="test",
            ),
            Resource(
                id="resource.b",
                name="b",
                type="test",
                provider="test",
            ),
        ],
        relationships=[
            Relationship(
                source_id="resource.a",
                target_id="resource.b",
                relationship_type="references",
            ),
        ],
    )

    candidate = InvestigationCandidate(
        resource_id="resource.b",
        candidate_type=CandidateType.ENTRY_POINT,
        reason="Test candidate.",
    )

    context = CandidateContextEngine().build(
        investigation,
        candidate,
    )

    assert len(context.related_resources) == 1
    assert context.related_resources[0].resource_id == "resource.a"
    assert context.related_resources[0].direction == "incoming"

    relationship = investigation.relationships[0]

    assert relationship.source_id == "resource.a"
    assert relationship.target_id == "resource.b"


def test_candidate_without_relationships_gets_explicit_context() -> None:
    investigation = Investigation(
        resources=[
            Resource(
                id="resource.a",
                name="a",
                type="test",
                provider="test",
            ),
        ],
    )

    candidate = InvestigationCandidate(
        resource_id="resource.a",
        candidate_type=CandidateType.ENTRY_POINT,
        reason="Suspicious configuration detected.",
    )

    context = CandidateContextEngine().build(
        investigation,
        candidate,
    )

    assert context.related_resources == []
    assert "no directly related infrastructure resources" in (context.explanation)

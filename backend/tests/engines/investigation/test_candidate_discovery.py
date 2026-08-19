from app.domain.models.finding import Finding
from app.domain.models.investigation import Investigation
from app.domain.models.resource import Resource
from app.engines.investigation.discovery.candidate_discovery import (
    InvestigationCandidateDiscovery,
)
from app.engines.investigation.models.candidate import CandidateType


def test_finding_resource_becomes_compromise_candidate() -> None:
    investigation = Investigation(
        resources=[
            Resource(
                id="aws_instance.web",
                name="web",
                type="aws_instance",
                provider="terraform",
            ),
        ],
        findings=[
            Finding(
                id="TF001",
                title="Public workload",
                description="Workload is publicly exposed.",
                severity="HIGH",
                resource_id="aws_instance.web",
                recommendation="Restrict public exposure.",
            ),
        ],
    )

    candidates = InvestigationCandidateDiscovery().discover(
        investigation,
    )

    assert len(candidates) == 1

    candidate = candidates[0]

    assert candidate.resource_id == "aws_instance.web"
    assert candidate.candidate_type == CandidateType.COMPROMISE_ANCHOR
    assert candidate.confidence == 0.90
    assert "resource_has_security_finding" in candidate.evidence


def test_public_security_group_becomes_entry_point_candidate() -> None:
    investigation = Investigation(
        resources=[
            Resource(
                id="aws_security_group.web",
                name="web",
                type="aws_security_group",
                provider="terraform",
                metadata={
                    "ingress": [
                        {
                            "from_port": 80,
                            "to_port": 80,
                            "protocol": '"tcp"',
                            "cidr_blocks": ['"0.0.0.0/0"'],
                        },
                        {
                            "from_port": 443,
                            "to_port": 443,
                            "protocol": '"tcp"',
                            "cidr_blocks": ['"0.0.0.0/0"'],
                        },
                    ],
                },
            ),
        ],
    )

    candidates = InvestigationCandidateDiscovery().discover(
        investigation,
    )

    assert len(candidates) == 1

    candidate = candidates[0]

    assert candidate.resource_id == "aws_security_group.web"
    assert candidate.candidate_type == CandidateType.ENTRY_POINT
    assert candidate.confidence == 0.85
    assert "ingress_allows_0.0.0.0/0" in candidate.evidence
    assert "public_ingress=tcp:80-80" in candidate.evidence
    assert "public_ingress=tcp:443-443" in candidate.evidence


def test_private_security_group_is_not_entry_point() -> None:
    investigation = Investigation(
        resources=[
            Resource(
                id="aws_security_group.internal",
                name="internal",
                type="aws_security_group",
                provider="terraform",
                metadata={
                    "ingress": [
                        {
                            "from_port": 443,
                            "to_port": 443,
                            "protocol": "tcp",
                            "cidr_blocks": ["10.0.0.0/16"],
                        },
                    ],
                },
            ),
        ],
    )

    candidates = InvestigationCandidateDiscovery().discover(
        investigation,
    )

    assert candidates == []


def test_resource_without_finding_or_network_exposure_is_not_candidate() -> None:
    investigation = Investigation(
        resources=[
            Resource(
                id="aws_instance.web",
                name="web",
                type="aws_instance",
                provider="terraform",
            ),
        ],
    )

    candidates = InvestigationCandidateDiscovery().discover(
        investigation,
    )

    assert candidates == []

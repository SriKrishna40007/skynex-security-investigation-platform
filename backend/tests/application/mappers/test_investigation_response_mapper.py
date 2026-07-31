from app.application.mappers import InvestigationResponseMapper
from app.domain.models import AttackPath, RiskAssessment
from app.domain.models.investigation import Investigation
from app.engines.blast_radius.models import (
    BlastRadiusAnalysis,
    BlastRadiusImpact,
)


def _rich_investigation() -> Investigation:
    investigation = Investigation(
        risk_score=55.0,
        summary="Canonical security investigation.",
    )

    investigation.analysis["attack_path"] = AttackPath(
        source="external-user",
        target="sensitive-data",
        nodes=[
            "external-user",
            "application",
            "privileged-role",
            "sensitive-data",
        ],
        hop_count=3,
        risk="CRITICAL",
        description=("Attack path contains high-impact security relationships."),
        exists=True,
    )

    investigation.analysis["blast_radius"] = [
        "external-user",
        "application",
        "privileged-role",
        "sensitive-data",
    ]

    investigation.analysis["blast_radius_analysis"] = BlastRadiusAnalysis(
        compromised_resource="external-user",
        reachable_resources=(
            "external-user",
            "application",
            "privileged-role",
            "sensitive-data",
        ),
        impacts=(
            BlastRadiusImpact(
                resource_id="external-user",
                depth=0,
            ),
            BlastRadiusImpact(
                resource_id="application",
                depth=1,
                relationship_types=("connects",),
            ),
            BlastRadiusImpact(
                resource_id="privileged-role",
                depth=2,
                relationship_types=(
                    "connects",
                    "allows_assume_role",
                ),
            ),
            BlastRadiusImpact(
                resource_id="sensitive-data",
                depth=3,
                relationship_types=(
                    "connects",
                    "allows_assume_role",
                    "allows_action",
                ),
            ),
        ),
    )

    investigation.analysis["risk"] = RiskAssessment(
        score=55,
        severity="MEDIUM",
        reasons=[
            "Critical semantic attack path detected.",
            "Compromise may affect 3 additional resources.",
        ],
    )

    return investigation


def test_mapper_preserves_legacy_response_contract():
    response = InvestigationResponseMapper().map(_rich_investigation())

    assert response.attack_path == [
        "external-user",
        "application",
        "privileged-role",
        "sensitive-data",
    ]

    assert response.blast_radius == [
        "external-user",
        "application",
        "privileged-role",
        "sensitive-data",
    ]

    assert response.risk_score == 55.0
    assert response.summary == "Canonical security investigation."


def test_mapper_exposes_semantic_attack_path():
    response = InvestigationResponseMapper().map(_rich_investigation())

    analysis = response.attack_path_analysis

    assert analysis is not None
    assert analysis.exists is True
    assert analysis.source == "external-user"
    assert analysis.target == "sensitive-data"
    assert analysis.hop_count == 3
    assert analysis.risk == "CRITICAL"


def test_mapper_exposes_evidence_aware_blast_radius():
    response = InvestigationResponseMapper().map(_rich_investigation())

    analysis = response.blast_radius_analysis

    assert analysis is not None
    assert analysis.compromised_resource == "external-user"
    assert analysis.affected_resource_count == 3
    assert analysis.maximum_depth == 3

    assert analysis.impacts[-1].relationship_types == [
        "connects",
        "allows_assume_role",
        "allows_action",
    ]


def test_mapper_exposes_canonical_risk():
    response = InvestigationResponseMapper().map(_rich_investigation())

    assert response.risk is not None
    assert response.risk.score == 55
    assert response.risk.severity == "MEDIUM"
    assert response.risk.reasons


def test_mapper_generates_reasoning_from_analysis_context():
    response = InvestigationResponseMapper().map(_rich_investigation())

    assert response.reasoning is not None

    assert any(
        "external-user" in finding and "sensitive-data" in finding
        for finding in response.reasoning.findings
    )

    assert any(
        "3 additional resource" in finding for finding in response.reasoning.findings
    )

    assert response.reasoning.recommendations
    assert response.reasoning.severity == "MEDIUM"


def test_mapper_handles_empty_investigation_safely():
    response = InvestigationResponseMapper().map(Investigation())

    assert response.attack_path == []
    assert response.blast_radius == []
    assert response.risk_score == 0.0

    assert response.attack_path_analysis is None
    assert response.blast_radius_analysis is None
    assert response.risk is None

    assert response.reasoning is not None
    assert response.reasoning.findings == []
    assert response.reasoning.recommendations == []
    assert response.reasoning.severity == "LOW"


def test_mapper_response_is_json_serializable():
    response = InvestigationResponseMapper().map(_rich_investigation())

    payload = response.model_dump(mode="json")

    assert payload["attack_path_analysis"]["risk"] == "CRITICAL"

    assert payload["blast_radius_analysis"]["affected_resource_count"] == 3

    assert payload["risk"]["severity"] == "MEDIUM"
    assert payload["reasoning"]["severity"] == "MEDIUM"

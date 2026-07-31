from app.schemas.investigation import (
    AttackPathAnalysisResponse,
    BlastRadiusAnalysisResponse,
    BlastRadiusImpactResponse,
    InvestigationResponse,
    ReasoningResponse,
    RiskAssessmentResponse,
)


def test_legacy_investigation_response_contract_is_preserved():
    response = InvestigationResponse(
        attack_path=["identity", "role", "secret"],
        blast_radius=["identity", "role", "secret"],
        risk_score=55.0,
        summary="Security investigation completed.",
    )

    assert response.attack_path == [
        "identity",
        "role",
        "secret",
    ]
    assert response.blast_radius == [
        "identity",
        "role",
        "secret",
    ]
    assert response.risk_score == 55.0
    assert response.summary == "Security investigation completed."

    assert response.attack_path_analysis is None
    assert response.blast_radius_analysis is None
    assert response.risk is None
    assert response.reasoning is None


def test_attack_path_analysis_response_exposes_semantic_evidence():
    response = AttackPathAnalysisResponse(
        source="external-user",
        target="production-secret",
        nodes=[
            "external-user",
            "application",
            "privileged-role",
            "production-secret",
        ],
        hop_count=3,
        risk="CRITICAL",
        description="Privilege-bearing attack path.",
        exists=True,
    )

    assert response.source == "external-user"
    assert response.target == "production-secret"
    assert response.hop_count == 3
    assert response.risk == "CRITICAL"
    assert response.exists is True


def test_blast_radius_analysis_response_exposes_propagation_evidence():
    response = BlastRadiusAnalysisResponse(
        compromised_resource="external-user",
        reachable_resources=[
            "external-user",
            "application",
            "privileged-role",
        ],
        affected_resource_count=2,
        maximum_depth=2,
        impacts=[
            BlastRadiusImpactResponse(
                resource_id="privileged-role",
                depth=2,
                relationship_types=[
                    "connects",
                    "allows_assume_role",
                ],
            )
        ],
    )

    assert response.affected_resource_count == 2
    assert response.maximum_depth == 2

    impact = response.impacts[0]

    assert impact.resource_id == "privileged-role"
    assert impact.depth == 2
    assert impact.relationship_types == [
        "connects",
        "allows_assume_role",
    ]


def test_risk_response_exposes_canonical_assessment():
    response = RiskAssessmentResponse(
        score=55,
        severity="MEDIUM",
        reasons=[
            "Critical semantic attack path detected.",
            "Compromise may affect additional resources.",
        ],
    )

    assert response.score == 55
    assert response.severity == "MEDIUM"
    assert len(response.reasons) == 2


def test_reasoning_response_exposes_investigator_guidance():
    response = ReasoningResponse(
        findings=[
            "Attack path identified.",
            "Compromise propagation detected.",
        ],
        recommendations=[
            "Break the highest-risk relationship.",
        ],
        severity="HIGH",
    )

    assert response.findings == [
        "Attack path identified.",
        "Compromise propagation detected.",
    ]
    assert response.recommendations == [
        "Break the highest-risk relationship.",
    ]
    assert response.severity == "HIGH"


def test_complete_investigation_response_supports_rich_contract():
    response = InvestigationResponse(
        attack_path=[
            "external-user",
            "privileged-role",
        ],
        blast_radius=[
            "external-user",
            "privileged-role",
        ],
        risk_score=40.0,
        summary="Investigation complete.",
        attack_path_analysis=AttackPathAnalysisResponse(
            source="external-user",
            target="privileged-role",
            nodes=[
                "external-user",
                "privileged-role",
            ],
            hop_count=1,
            risk="HIGH",
            exists=True,
        ),
        blast_radius_analysis=BlastRadiusAnalysisResponse(
            compromised_resource="external-user",
            reachable_resources=[
                "external-user",
                "privileged-role",
            ],
            affected_resource_count=1,
            maximum_depth=1,
        ),
        risk=RiskAssessmentResponse(
            score=40,
            severity="MEDIUM",
            reasons=[
                "Security topology contains elevated risk.",
            ],
        ),
        reasoning=ReasoningResponse(
            findings=[
                "Privilege-bearing relationship detected.",
            ],
            recommendations=[
                "Restrict the authorization relationship.",
            ],
            severity="MEDIUM",
        ),
    )

    assert response.attack_path_analysis is not None
    assert response.attack_path_analysis.exists is True

    assert response.blast_radius_analysis is not None
    assert response.blast_radius_analysis.affected_resource_count == 1

    assert response.risk is not None
    assert response.risk.score == 40

    assert response.reasoning is not None
    assert response.reasoning.severity == "MEDIUM"


def test_response_mutable_defaults_are_isolated():
    first = InvestigationResponse()
    second = InvestigationResponse()

    first.attack_path.append("identity")
    first.blast_radius.append("role")

    assert second.attack_path == []
    assert second.blast_radius == []

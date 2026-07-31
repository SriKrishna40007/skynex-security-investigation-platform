from app.application.context import AnalysisContextBuilder
from app.application.pipeline import InvestigationPipeline
from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.ai.reasoning.reasoning_engine import ReasoningEngine


def _security_investigation() -> Investigation:
    investigation = Investigation()

    investigation.resources = [
        Resource(
            id="external-user",
            name="External User",
            type="identity",
            provider="canonical",
        ),
        Resource(
            id="application",
            name="Application",
            type="application",
            provider="canonical",
        ),
        Resource(
            id="privileged-role",
            name="Privileged Role",
            type="identity",
            provider="canonical",
        ),
        Resource(
            id="sensitive-data",
            name="Sensitive Data",
            type="data",
            provider="canonical",
        ),
    ]

    investigation.relationships = [
        Relationship(
            source_id="external-user",
            target_id="application",
            relationship_type="connects",
        ),
        Relationship(
            source_id="application",
            target_id="privileged-role",
            relationship_type="allows_assume_role",
        ),
        Relationship(
            source_id="privileged-role",
            target_id="sensitive-data",
            relationship_type="allows_action",
        ),
    ]

    return investigation


def _execute_reasoning():
    investigation = _security_investigation()

    result = InvestigationPipeline().execute(
        investigation,
        source="external-user",
        target="sensitive-data",
        compromised_resource="external-user",
    )

    context = AnalysisContextBuilder().build(result)

    evidence = ReasoningEngine().analyze(context)

    return result, context, evidence


def test_pipeline_security_analysis_reaches_reasoning_layer():
    result, context, evidence = _execute_reasoning()

    assert result.analysis["attack_path"].exists

    assert result.analysis["blast_radius_analysis"].affected_resource_count == 3

    assert result.analysis["risk"].score > 0

    assert context.attack_path is result.analysis["attack_path"]

    assert context.blast_radius_analysis is result.analysis["blast_radius_analysis"]

    assert context.risk is result.analysis["risk"]

    assert evidence.findings


def test_reasoning_explains_pipeline_attack_path():
    _, _, evidence = _execute_reasoning()

    assert any(
        "external-user" in finding
        and "sensitive-data" in finding
        and "3 hop" in finding
        for finding in evidence.findings
    )


def test_reasoning_explains_pipeline_blast_radius():
    _, _, evidence = _execute_reasoning()

    assert any(
        "3 additional resource" in finding and "depth of 3" in finding
        for finding in evidence.findings
    )

    assert any(
        "connects" in finding
        and "allows_assume_role" in finding
        and "allows_action" in finding
        for finding in evidence.findings
    )


def test_reasoning_severity_matches_canonical_risk():
    _, context, evidence = _execute_reasoning()

    assert context.risk is not None
    assert evidence.severity == context.risk.severity


def test_reasoning_integration_remains_provider_neutral():
    _, _, evidence = _execute_reasoning()

    rendered = " ".join(
        [
            *evidence.findings,
            *evidence.recommendations,
        ]
    ).lower()

    assert "terraform" not in rendered
    assert "aws" not in rendered
    assert "iam intelligence engine" not in rendered

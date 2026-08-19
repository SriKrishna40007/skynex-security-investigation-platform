from app.domain.models.finding import Finding
from app.engines.remediation import RemediationEngine


def test_generates_remediation_plan_from_canonical_finding() -> None:
    finding = Finding(
        id="finding-001",
        title="Overly permissive IAM policy",
        description="Policy grants excessive permissions.",
        severity="HIGH",
        resource_id="policy/admin",
        recommendation="Restrict the policy to required actions.",
    )

    plan = RemediationEngine().generate(finding)

    assert plan.finding_id == "finding-001"
    assert plan.title == "Overly permissive IAM policy"
    assert plan.severity == "HIGH"
    assert plan.resource_id == "policy/admin"
    assert plan.executable is False
    assert plan.steps[0] == "Restrict the policy to required actions."
    assert len(plan.steps) == 2


def test_generates_safe_default_when_recommendation_is_empty() -> None:
    finding = Finding(
        id="finding-002",
        title="Security finding",
        description="Finding without recommendation.",
        severity="MEDIUM",
        resource_id="resource/example",
        recommendation="",
    )

    plan = RemediationEngine().generate(finding)

    assert plan.executable is False
    assert len(plan.steps) == 2
    assert "least-privilege" in plan.steps[0]

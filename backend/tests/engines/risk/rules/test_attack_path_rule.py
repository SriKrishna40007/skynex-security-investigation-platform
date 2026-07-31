from app.domain.models.attack_path import AttackPath
from app.domain.models.investigation import Investigation
from app.engines.risk.rules import AttackPathRule


def _investigation_with_attack_path(
    *,
    exists: bool = True,
    risk: str = "HIGH",
    description: str = "Security-significant attack path detected.",
) -> Investigation:
    investigation = Investigation()

    investigation.analysis["attack_path"] = AttackPath(
        source="source",
        target="target",
        nodes=["source", "target"] if exists else [],
        hop_count=1 if exists else 0,
        risk=risk,
        description=description,
        exists=exists,
    )

    return investigation


def test_missing_attack_path_contributes_no_risk():
    score, reasons = AttackPathRule().evaluate(Investigation())

    assert score == 0
    assert reasons == []


def test_nonexistent_attack_path_contributes_no_risk():
    investigation = _investigation_with_attack_path(
        exists=False,
    )

    score, reasons = AttackPathRule().evaluate(investigation)

    assert score == 0
    assert reasons == []


def test_medium_attack_path_uses_semantic_severity():
    investigation = _investigation_with_attack_path(
        risk="MEDIUM",
    )

    score, reasons = AttackPathRule().evaluate(investigation)

    assert score == 20
    assert reasons


def test_high_attack_path_preserves_existing_score():
    investigation = _investigation_with_attack_path(
        risk="HIGH",
    )

    score, reasons = AttackPathRule().evaluate(investigation)

    assert score == 30
    assert reasons


def test_critical_attack_path_scores_above_high():
    investigation = _investigation_with_attack_path(
        risk="CRITICAL",
    )

    score, reasons = AttackPathRule().evaluate(investigation)

    assert score == 40
    assert reasons


def test_attack_path_reason_preserves_semantic_explanation():
    description = (
        "Attack path contains security-significant relationships "
        "that can enable privileged or sensitive access."
    )

    investigation = _investigation_with_attack_path(
        risk="HIGH",
        description=description,
    )

    _, reasons = AttackPathRule().evaluate(investigation)

    assert any(description in reason for reason in reasons)


def test_unknown_attack_path_severity_fails_safe():
    investigation = _investigation_with_attack_path(
        risk="UNRECOGNIZED",
    )

    score, reasons = AttackPathRule().evaluate(investigation)

    assert score == 0
    assert reasons

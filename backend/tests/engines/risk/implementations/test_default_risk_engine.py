from dataclasses import dataclass

from app.domain.models.investigation import Investigation
from app.engines.risk.implementations import DefaultRiskEngine


@dataclass
class AttackPathStub:
    exists: bool
    risk: str
    source: str = "source"
    target: str = "target"
    description: str = ""


def test_engine_aggregates_attack_path_and_blast_radius_risk():
    investigation = Investigation()

    investigation.analysis["attack_path"] = AttackPathStub(
        exists=True,
        risk="HIGH",
    )

    investigation.analysis["blast_radius"] = [
        "source",
        "resource-a",
        "resource-b",
    ]

    result = DefaultRiskEngine().analyze(investigation)

    assessment = result.analysis["risk"]

    # HIGH attack path = 30
    # Legacy blast radius with 3 resources = 15
    assert assessment.score == 45
    assert assessment.severity == "MEDIUM"

    assert any("HIGH attack path" in reason for reason in assessment.reasons)

    assert any("Legacy blast-radius" in reason for reason in assessment.reasons)


def test_engine_preserves_zero_risk_when_no_evidence_exists():
    investigation = Investigation()

    result = DefaultRiskEngine().analyze(investigation)

    assessment = result.analysis["risk"]

    assert assessment.score == 0
    assert assessment.severity == "LOW"
    assert assessment.reasons == []


def test_engine_caps_aggregated_score_at_100():
    investigation = Investigation()

    class MaximumRule:
        def evaluate(self, investigation):
            return 80, ["Maximum synthetic contribution."]

    engine = DefaultRiskEngine()
    engine._rules = [
        MaximumRule(),
        MaximumRule(),
    ]

    result = engine.analyze(investigation)

    assessment = result.analysis["risk"]

    assert assessment.score == 100
    assert assessment.severity == "CRITICAL"


def test_engine_severity_thresholds_are_stable():
    expected = {
        0: "LOW",
        29: "LOW",
        30: "MEDIUM",
        59: "MEDIUM",
        60: "HIGH",
        79: "HIGH",
        80: "CRITICAL",
        100: "CRITICAL",
    }

    class FixedRule:
        def __init__(self, score):
            self.score = score

        def evaluate(self, investigation):
            return self.score, []

    for score, severity in expected.items():
        engine = DefaultRiskEngine()
        engine._rules = [FixedRule(score)]

        investigation = engine.analyze(Investigation())

        assert investigation.analysis["risk"].score == score
        assert investigation.analysis["risk"].severity == severity


def test_topology_risk_does_not_overwrite_existing_investigation_risk_score():
    investigation = Investigation(
        risk_score=55.0,
    )

    investigation.analysis["attack_path"] = AttackPathStub(
        exists=True,
        risk="HIGH",
    )

    result = DefaultRiskEngine().analyze(investigation)

    assert result.analysis["risk"].score == 30

    # risk_score may contain upstream/provider analysis such as IAM engine
    # evidence. Topology risk remains a separate canonical assessment.
    assert result.risk_score == 55.0

from app.application.context import AnalysisContext
from app.domain.models.attack_path import AttackPath
from app.domain.models import RiskAssessment
from app.engines.ai.reasoning.reasoning_engine import ReasoningEngine
from app.engines.blast_radius.models import (
    BlastRadiusAnalysis,
    BlastRadiusImpact,
)


def test_reasoning_explains_semantic_attack_path():
    context = AnalysisContext(
        attack_path=AttackPath(
            source="identity",
            target="secret",
            nodes=[
                "identity",
                "role",
                "secret",
            ],
            hop_count=2,
            risk="HIGH",
            description=("Path contains privilege-bearing authorization semantics."),
            exists=True,
        )
    )

    evidence = ReasoningEngine().analyze(context)

    assert any(
        "identity" in finding
        and "secret" in finding
        and "2 hop" in finding
        and "HIGH" in finding
        for finding in evidence.findings
    )

    assert (
        "Path contains privilege-bearing authorization semantics." in evidence.findings
    )


def test_reasoning_explains_rich_blast_radius():
    analysis = BlastRadiusAnalysis(
        compromised_resource="identity",
        reachable_resources=(
            "identity",
            "role",
            "secret",
        ),
        impacts=(
            BlastRadiusImpact(
                resource_id="identity",
                depth=0,
            ),
            BlastRadiusImpact(
                resource_id="role",
                depth=1,
                relationship_types=("allows_assume_role",),
            ),
            BlastRadiusImpact(
                resource_id="secret",
                depth=2,
                relationship_types=(
                    "allows_assume_role",
                    "allows_action",
                ),
            ),
        ),
    )

    context = AnalysisContext(
        blast_radius=[
            "identity",
            "role",
            "secret",
        ],
        blast_radius_analysis=analysis,
    )

    evidence = ReasoningEngine().analyze(context)

    assert any(
        "2 additional resource" in finding and "depth of 2" in finding
        for finding in evidence.findings
    )

    assert any(
        "allows_assume_role" in finding and "allows_action" in finding
        for finding in evidence.findings
    )


def test_reasoning_preserves_legacy_blast_radius_fallback():
    context = AnalysisContext(
        blast_radius=[
            "source",
            "target",
        ],
    )

    evidence = ReasoningEngine().analyze(context)

    assert "Blast radius includes 2 resources." in evidence.findings


def test_reasoning_uses_canonical_risk_assessment():
    context = AnalysisContext(
        risk=RiskAssessment(
            score=30,
            severity="HIGH",
            reasons=[
                "High-risk authorization path detected.",
            ],
        )
    )

    evidence = ReasoningEngine().analyze(context)

    assert evidence.severity == "HIGH"

    assert "High-risk authorization path detected." in evidence.findings


def test_reasoning_does_not_fabricate_security_evidence():
    context = AnalysisContext()

    evidence = ReasoningEngine().analyze(context)

    assert evidence.findings == []
    assert evidence.recommendations == []

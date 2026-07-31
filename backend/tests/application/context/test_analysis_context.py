from app.application.context import AnalysisContext
from app.engines.blast_radius.models import (
    BlastRadiusAnalysis,
    BlastRadiusImpact,
)


def test_analysis_context_accepts_rich_blast_radius_evidence():
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

    assert context.blast_radius == [
        "identity",
        "role",
        "secret",
    ]

    assert context.blast_radius_analysis is analysis
    assert context.blast_radius_analysis.affected_resource_count == 2
    assert context.blast_radius_analysis.maximum_depth == 2


def test_analysis_context_preserves_legacy_blast_radius_contract():
    context = AnalysisContext(
        blast_radius=[
            "source",
            "target",
        ],
    )

    assert context.blast_radius == [
        "source",
        "target",
    ]

    assert context.blast_radius_analysis is None

from app.application.context import AnalysisContextBuilder
from app.domain.models.investigation import Investigation
from app.engines.blast_radius.models import (
    BlastRadiusAnalysis,
    BlastRadiusImpact,
)


def test_context_builder_transports_rich_blast_radius_evidence():
    investigation = Investigation()

    analysis = BlastRadiusAnalysis(
        compromised_resource="identity",
        reachable_resources=(
            "identity",
            "role",
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
        ),
    )

    investigation.analysis["blast_radius"] = [
        "identity",
        "role",
    ]

    investigation.analysis["blast_radius_analysis"] = analysis

    context = AnalysisContextBuilder().build(
        investigation,
    )

    assert context.blast_radius == [
        "identity",
        "role",
    ]

    assert context.blast_radius_analysis is analysis
    assert context.blast_radius_analysis.affected_resource_count == 1
    assert context.blast_radius_analysis.maximum_depth == 1


def test_context_builder_handles_missing_rich_blast_radius_evidence():
    investigation = Investigation()

    investigation.analysis["blast_radius"] = [
        "identity",
    ]

    context = AnalysisContextBuilder().build(
        investigation,
    )

    assert context.blast_radius == [
        "identity",
    ]

    assert context.blast_radius_analysis is None

from app.engines.blast_radius.models import (
    BlastRadiusAnalysis,
    BlastRadiusImpact,
)


def test_blast_radius_analysis_describes_propagation():
    analysis = BlastRadiusAnalysis(
        compromised_resource="internet",
        reachable_resources=(
            "internet",
            "service",
            "database",
        ),
        impacts=(
            BlastRadiusImpact(
                resource_id="internet",
                depth=0,
            ),
            BlastRadiusImpact(
                resource_id="service",
                depth=1,
                relationship_types=("connects",),
            ),
            BlastRadiusImpact(
                resource_id="database",
                depth=2,
                relationship_types=(
                    "connects",
                    "allows_action",
                ),
            ),
        ),
    )

    assert analysis.compromised_resource == "internet"

    assert analysis.reachable_resources == (
        "internet",
        "service",
        "database",
    )

    assert analysis.affected_resource_count == 2
    assert analysis.maximum_depth == 2


def test_compromised_resource_is_not_counted_as_affected():
    analysis = BlastRadiusAnalysis(
        compromised_resource="role",
        reachable_resources=("role",),
        impacts=(
            BlastRadiusImpact(
                resource_id="role",
                depth=0,
            ),
        ),
    )

    assert analysis.affected_resource_count == 0
    assert analysis.maximum_depth == 0


def test_empty_impact_evidence_has_zero_depth():
    analysis = BlastRadiusAnalysis(
        compromised_resource="missing",
        reachable_resources=(),
        impacts=(),
    )

    assert analysis.affected_resource_count == 0
    assert analysis.maximum_depth == 0


def test_blast_radius_model_is_provider_neutral():
    impact = BlastRadiusImpact(
        resource_id="canonical-resource",
        depth=1,
        relationship_types=("allows_action",),
    )

    analysis = BlastRadiusAnalysis(
        compromised_resource="canonical-source",
        reachable_resources=(
            "canonical-source",
            "canonical-resource",
        ),
        impacts=(impact,),
    )

    assert analysis.affected_resource_count == 1
    assert impact.relationship_types == ("allows_action",)

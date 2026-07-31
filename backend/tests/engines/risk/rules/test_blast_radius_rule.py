from app.domain.models.investigation import Investigation
from app.engines.blast_radius.models import (
    BlastRadiusAnalysis,
    BlastRadiusImpact,
)
from app.engines.risk.rules import BlastRadiusRule


def _rich_investigation(
    *,
    reachable_resources: tuple[str, ...],
    impacts: tuple[BlastRadiusImpact, ...],
) -> Investigation:
    investigation = Investigation()

    investigation.analysis["blast_radius"] = list(reachable_resources)

    investigation.analysis["blast_radius_analysis"] = BlastRadiusAnalysis(
        compromised_resource="source",
        reachable_resources=reachable_resources,
        impacts=impacts,
    )

    return investigation


def test_missing_blast_radius_contributes_no_risk():
    score, reasons = BlastRadiusRule().evaluate(Investigation())

    assert score == 0
    assert reasons == []


def test_only_compromised_resource_contributes_no_risk():
    investigation = _rich_investigation(
        reachable_resources=("source",),
        impacts=(
            BlastRadiusImpact(
                resource_id="source",
                depth=0,
            ),
        ),
    )

    score, reasons = BlastRadiusRule().evaluate(investigation)

    assert score == 0
    assert reasons == []


def test_rich_analysis_counts_only_affected_resources():
    investigation = _rich_investigation(
        reachable_resources=(
            "source",
            "role",
            "secret",
        ),
        impacts=(
            BlastRadiusImpact(
                resource_id="source",
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

    score, reasons = BlastRadiusRule().evaluate(investigation)

    assert score == 10
    assert reasons
    assert any("2" in reason for reason in reasons)


def test_rich_analysis_exposes_propagation_depth():
    investigation = _rich_investigation(
        reachable_resources=(
            "source",
            "application",
            "role",
            "secret",
        ),
        impacts=(
            BlastRadiusImpact(
                resource_id="source",
                depth=0,
            ),
            BlastRadiusImpact(
                resource_id="application",
                depth=1,
                relationship_types=("connects",),
            ),
            BlastRadiusImpact(
                resource_id="role",
                depth=2,
                relationship_types=(
                    "connects",
                    "allows_assume_role",
                ),
            ),
            BlastRadiusImpact(
                resource_id="secret",
                depth=3,
                relationship_types=(
                    "connects",
                    "allows_assume_role",
                    "allows_action",
                ),
            ),
        ),
    )

    score, reasons = BlastRadiusRule().evaluate(investigation)

    assert score == 15
    assert any("depth 3" in reason.lower() for reason in reasons)


def test_legacy_blast_radius_contract_remains_supported():
    investigation = Investigation()

    investigation.analysis["blast_radius"] = [
        "source",
        "resource-a",
        "resource-b",
    ]

    score, reasons = BlastRadiusRule().evaluate(investigation)

    assert score == 15
    assert reasons


def test_blast_radius_score_remains_capped():
    reachable = tuple(["source"] + [f"resource-{index}" for index in range(20)])

    impacts = tuple(
        [
            BlastRadiusImpact(
                resource_id="source",
                depth=0,
            )
        ]
        + [
            BlastRadiusImpact(
                resource_id=f"resource-{index}",
                depth=1,
                relationship_types=("connects",),
            )
            for index in range(20)
        ]
    )

    investigation = _rich_investigation(
        reachable_resources=reachable,
        impacts=impacts,
    )

    score, _ = BlastRadiusRule().evaluate(investigation)

    assert score == 30

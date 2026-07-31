from app.application.pipeline import InvestigationPipeline
from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource


def test_pipeline_builds_complete_investigation():
    investigation = Investigation()

    investigation.resources = [
        Resource(
            id="internet",
            name="Internet",
            type="external",
            provider="external",
            metadata={
                "references": [
                    "alb",
                ],
            },
        ),
        Resource(
            id="alb",
            name="ALB",
            type="aws_lb",
            provider="aws",
            metadata={
                "references": [
                    "ec2",
                ],
            },
        ),
        Resource(
            id="ec2",
            name="EC2",
            type="aws_instance",
            provider="aws",
        ),
    ]

    pipeline = InvestigationPipeline()

    result = pipeline.run(
        investigation,
        source="internet",
        target="ec2",
    )

    assert "knowledge_graph" in result.analysis
    assert "attack_path" in result.analysis
    assert "blast_radius" in result.analysis

    attack_path = result.analysis["attack_path"]

    assert attack_path.exists is True
    assert attack_path.nodes == [
        "internet",
        "alb",
        "ec2",
    ]
    assert attack_path.hop_count == 2

    assert result.analysis["blast_radius"] == [
        "internet",
        "alb",
        "ec2",
    ]


def test_pipeline_does_not_fabricate_topology_for_iam_investigation():
    from app.application.pipeline.investigation_pipeline import (
        InvestigationPipeline,
    )
    from app.domain.models.investigation import Investigation
    from app.domain.models.resource import Resource

    investigation = Investigation(
        resources=[
            Resource(
                id="aws.iam_policy.example",
                name="Example IAM Policy",
                type="iam_policy",
                provider="aws",
            )
        ],
        risk_score=55.0,
    )

    pipeline = InvestigationPipeline()

    result = pipeline.execute(investigation)

    assert result.graph is None
    assert result.relationships == []
    assert "attack_path" not in result.analysis
    assert "blast_radius" not in result.analysis
    assert result.risk_score == 55.0


def test_pipeline_preserves_iam_analysis_without_topology():
    from app.application.pipeline.investigation_pipeline import (
        InvestigationPipeline,
    )
    from app.domain.models.investigation import Investigation

    investigation = Investigation(
        risk_score=55.0,
        analysis={
            "iam": {
                "overall_risk_score": 55,
                "finding_count": 3,
                "recommendations": [
                    "Apply least privilege.",
                ],
            }
        },
    )

    pipeline = InvestigationPipeline()

    result = pipeline.execute(investigation)

    assert result.analysis["iam"]["overall_risk_score"] == 55
    assert result.analysis["iam"]["finding_count"] == 3
    assert result.risk_score == 55.0
    assert result.graph is None


def test_pipeline_preserves_upstream_risk_score_when_topology_risk_is_generated():
    """
    Provider/integration risk and canonical topology risk are separate
    evidence channels.

    Pipeline topology analysis must not destroy an upstream risk score.
    """

    investigation = Investigation(
        risk_score=55.0,
    )

    investigation.resources = [
        Resource(
            id="source",
            name="Source",
            type="identity",
            provider="canonical",
        ),
        Resource(
            id="target",
            name="Target",
            type="resource",
            provider="canonical",
        ),
    ]

    investigation.relationships = [
        Relationship(
            source_id="source",
            target_id="target",
            relationship_type="allows_assume_role",
        ),
    ]

    result = InvestigationPipeline().execute(
        investigation,
        source="source",
        target="target",
        compromised_resource="source",
    )

    assert result.risk_score == 55.0

    assert "risk" in result.analysis

    topology_risk = result.analysis["risk"]

    assert topology_risk.score > 0
    assert topology_risk.severity in {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }

    assert topology_risk.reasons

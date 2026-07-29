from app.application.pipeline import InvestigationPipeline
from app.domain.models.investigation import Investigation
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

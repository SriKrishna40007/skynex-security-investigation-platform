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

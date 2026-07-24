from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.blast_radius.implementations import DefaultBlastRadiusEngine
from app.engines.graph.implementations import KnowledgeGraphEngine


def test_blast_radius_returns_all_reachable_resources():
    investigation = Investigation(
        id="investigation-1",
        name="Blast Radius Test",
    )

    investigation.resources = [
        Resource(
            id="internet",
            name="Internet",
            type="external",
            provider="external",
        ),
        Resource(
            id="alb",
            name="ALB",
            type="aws_lb",
            provider="aws",
        ),
        Resource(
            id="ec2",
            name="EC2",
            type="aws_instance",
            provider="aws",
        ),
        Resource(
            id="rds",
            name="RDS",
            type="aws_db_instance",
            provider="aws",
        ),
    ]

    investigation.relationships = [
        Relationship(
            source_id="internet",
            target_id="alb",
            relationship_type="connects",
        ),
        Relationship(
            source_id="alb",
            target_id="ec2",
            relationship_type="connects",
        ),
        Relationship(
            source_id="ec2",
            target_id="rds",
            relationship_type="connects",
        ),
    ]

    graph_engine = KnowledgeGraphEngine()
    investigation = graph_engine.build(investigation)

    blast_radius_engine = DefaultBlastRadiusEngine()
    result = blast_radius_engine.analyze(
        investigation,
        "internet",
    )

    assert result.analysis["blast_radius"] == {
        "internet",
        "alb",
        "ec2",
        "rds",
    }

from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.attack_path.implementations import DefaultAttackPathEngine
from app.engines.graph.implementations import KnowledgeGraphEngine


def test_attack_path_returns_shortest_path():
    investigation = Investigation(
        id="investigation-1",
        name="Attack Path Test",
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

    investigation = KnowledgeGraphEngine().build(investigation)

    result = DefaultAttackPathEngine().analyze(
        investigation,
        "internet",
        "rds",
    )

    assert result.analysis["attack_path"] == [
        "internet",
        "alb",
        "ec2",
        "rds",
    ]

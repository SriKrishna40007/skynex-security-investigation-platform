from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.graph.implementations import KnowledgeGraphEngine


def test_knowledge_graph_engine_builds_graph():
    investigation = Investigation(
        id="investigation-1",
        name="Knowledge Graph Test",
    )

    investigation.resources = [
        Resource(
            id="aws_instance.web",
            name="web",
            type="aws_instance",
            provider="aws",
        ),
        Resource(
            id="aws_security_group.web",
            name="web-sg",
            type="aws_security_group",
            provider="aws",
        ),
    ]

    investigation.relationships = [
        Relationship(
            source_id="aws_instance.web",
            target_id="aws_security_group.web",
            relationship_type="references",
        )
    ]

    engine = KnowledgeGraphEngine()

    result = engine.build(investigation)

    graph = result.analysis["knowledge_graph"]

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1

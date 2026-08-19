from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.blast_radius.implementations import DefaultBlastRadiusEngine
from app.engines.graph.models import GraphEdge, GraphNode, KnowledgeGraph
from app.engines.graph.implementations import KnowledgeGraphEngine


def test_blast_radius_returns_all_reachable_resources():
    investigation = Investigation()

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

    result = DefaultBlastRadiusEngine().analyze(
        investigation,
        "internet",
    )

    assert result.analysis["blast_radius"] == [
        "internet",
        "alb",
        "ec2",
        "rds",
    ]


def test_blast_radius_preserves_propagation_evidence():
    investigation = Investigation()

    investigation.resources = [
        Resource(
            id="internet",
            name="Internet",
            type="external",
            provider="external",
        ),
        Resource(
            id="service",
            name="Service",
            type="application",
            provider="canonical",
        ),
        Resource(
            id="database",
            name="Database",
            type="database",
            provider="canonical",
        ),
    ]

    investigation.relationships = [
        Relationship(
            source_id="internet",
            target_id="service",
            relationship_type="connects",
        ),
        Relationship(
            source_id="service",
            target_id="database",
            relationship_type="allows_action",
        ),
    ]

    investigation = KnowledgeGraphEngine().build(investigation)

    result = DefaultBlastRadiusEngine().analyze(
        investigation,
        "internet",
    )

    analysis = result.analysis["blast_radius_analysis"]

    assert result.analysis["blast_radius"] == [
        "internet",
        "service",
        "database",
    ]

    assert analysis.compromised_resource == "internet"

    assert analysis.reachable_resources == (
        "internet",
        "service",
        "database",
    )

    assert analysis.affected_resource_count == 2
    assert analysis.maximum_depth == 2

    assert [
        (
            impact.resource_id,
            impact.depth,
            impact.relationship_types,
        )
        for impact in analysis.impacts
    ] == [
        (
            "internet",
            0,
            (),
        ),
        (
            "service",
            1,
            ("connects",),
        ),
        (
            "database",
            2,
            (
                "connects",
                "allows_action",
            ),
        ),
    ]


def test_blast_radius_evidence_rejects_non_security_relationships():
    investigation = Investigation()

    investigation.resources = [
        Resource(
            id="source",
            name="Source",
            type="canonical",
            provider="canonical",
        ),
        Resource(
            id="reachable",
            name="Reachable",
            type="canonical",
            provider="canonical",
        ),
        Resource(
            id="metadata",
            name="Metadata",
            type="canonical",
            provider="canonical",
        ),
    ]

    investigation.relationships = [
        Relationship(
            source_id="source",
            target_id="reachable",
            relationship_type="connects",
        ),
        Relationship(
            source_id="reachable",
            target_id="metadata",
            relationship_type="descriptive_metadata",
        ),
    ]

    investigation = KnowledgeGraphEngine().build(investigation)

    result = DefaultBlastRadiusEngine().analyze(
        investigation,
        "source",
    )

    analysis = result.analysis["blast_radius_analysis"]

    assert result.analysis["blast_radius"] == [
        "source",
        "reachable",
    ]

    assert analysis.reachable_resources == (
        "source",
        "reachable",
    )

    assert analysis.affected_resource_count == 1
    assert analysis.maximum_depth == 1

    assert all(
        "descriptive_metadata" not in impact.relationship_types
        for impact in analysis.impacts
    )


def test_missing_compromised_resource_produces_empty_evidence():
    investigation = Investigation()

    investigation.resources = [
        Resource(
            id="resource",
            name="Resource",
            type="canonical",
            provider="canonical",
        ),
    ]

    investigation = KnowledgeGraphEngine().build(investigation)

    result = DefaultBlastRadiusEngine().analyze(
        investigation,
        "missing",
    )

    analysis = result.analysis["blast_radius_analysis"]

    assert result.analysis["blast_radius"] == []
    assert analysis.compromised_resource == "missing"
    assert analysis.reachable_resources == ()
    assert analysis.impacts == ()
    assert analysis.affected_resource_count == 0
    assert analysis.maximum_depth == 0


def test_blast_radius_analysis_uses_security_semantic_propagation():
    investigation = Investigation()

    investigation.resources = [
        Resource(
            id="instance",
            name="instance",
            type="aws_instance",
            provider="terraform",
        ),
        Resource(
            id="security_group",
            name="security_group",
            type="aws_security_group",
            provider="terraform",
        ),
        Resource(
            id="vpc",
            name="vpc",
            type="aws_vpc",
            provider="terraform",
        ),
        Resource(
            id="subnet",
            name="subnet",
            type="aws_subnet",
            provider="terraform",
        ),
    ]

    investigation.analysis["knowledge_graph"] = KnowledgeGraph()

    for resource in investigation.resources:
        investigation.analysis["knowledge_graph"].add_node(
            GraphNode(
                resource.id,
                resource.name,
                resource.type,
            )
        )

    graph = investigation.analysis["knowledge_graph"]

    graph.add_edge(
        GraphEdge(
            source="instance",
            target="security_group",
            relationship_type="protected_by",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="security_group",
            target="vpc",
            relationship_type="belongs_to",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="instance",
            target="subnet",
            relationship_type="deployed_in",
        )
    )

    result = DefaultBlastRadiusEngine().analyze(
        investigation,
        "security_group",
    )

    analysis = result.analysis["blast_radius_analysis"]

    assert analysis.reachable_resources == (
        "security_group",
        "vpc",
        "instance",
        "subnet",
    )

    assert analysis.affected_resource_count == 3

    impacts = {impact.resource_id: impact for impact in analysis.impacts}

    assert impacts["vpc"].depth == 1
    assert impacts["vpc"].relationship_types == ("belongs_to",)

    assert impacts["instance"].depth == 1
    assert impacts["instance"].relationship_types == ("protected_by",)

    assert impacts["subnet"].depth == 2
    assert impacts["subnet"].relationship_types == (
        "protected_by",
        "deployed_in",
    )

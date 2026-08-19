from app.engines.graph.models import GraphEdge, GraphNode, KnowledgeGraph
from app.engines.graph.traversal import SecurityNeighborResolver


def test_protected_by_resolves_reverse_security_neighbor():
    graph = KnowledgeGraph()

    graph.add_node(
        GraphNode(
            "instance",
            "Instance",
            "aws_instance",
        )
    )

    graph.add_node(
        GraphNode(
            "security_group",
            "Security Group",
            "aws_security_group",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="instance",
            target="security_group",
            relationship_type="protected_by",
        )
    )

    neighbors = SecurityNeighborResolver().resolve(
        graph,
        "security_group",
    )

    assert [
        (
            neighbor.resource_id,
            neighbor.relationship_type,
            neighbor.direction,
        )
        for neighbor in neighbors
    ] == [
        (
            "instance",
            "protected_by",
            "reverse",
        )
    ]


def test_forward_relationship_remains_forward():
    graph = KnowledgeGraph()

    graph.add_node(
        GraphNode(
            "subnet",
            "Subnet",
            "aws_subnet",
        )
    )

    graph.add_node(
        GraphNode(
            "vpc",
            "VPC",
            "aws_vpc",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="subnet",
            target="vpc",
            relationship_type="belongs_to",
        )
    )

    neighbors = SecurityNeighborResolver().resolve(
        graph,
        "subnet",
    )

    assert [
        (
            neighbor.resource_id,
            neighbor.relationship_type,
            neighbor.direction,
        )
        for neighbor in neighbors
    ] == [
        (
            "vpc",
            "belongs_to",
            "forward",
        )
    ]


def test_non_security_relationship_is_not_resolved():
    graph = KnowledgeGraph()

    graph.add_node(
        GraphNode(
            "service",
            "Service",
            "service",
        )
    )

    graph.add_node(
        GraphNode(
            "metadata",
            "Metadata",
            "metadata",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="service",
            target="metadata",
            relationship_type="descriptive_metadata",
        )
    )

    assert (
        SecurityNeighborResolver().resolve(
            graph,
            "service",
        )
        == []
    )

    assert (
        SecurityNeighborResolver().resolve(
            graph,
            "metadata",
        )
        == []
    )

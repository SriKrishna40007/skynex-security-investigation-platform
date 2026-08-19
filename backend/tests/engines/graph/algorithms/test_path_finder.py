from app.engines.graph.algorithms import PathFinder
from app.engines.graph.models import GraphEdge, GraphNode, KnowledgeGraph


def test_shortest_path_returns_expected_path():
    graph = KnowledgeGraph()

    graph.add_node(GraphNode("internet", "Internet", "external"))
    graph.add_node(GraphNode("alb", "ALB", "aws_lb"))
    graph.add_node(GraphNode("ec2", "EC2", "aws_instance"))
    graph.add_node(GraphNode("rds", "RDS", "aws_db_instance"))

    graph.add_edge(
        GraphEdge(
            source="internet",
            target="alb",
            relationship_type="connects",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="alb",
            target="ec2",
            relationship_type="connects",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="ec2",
            target="rds",
            relationship_type="connects",
        )
    )

    path_finder = PathFinder()

    path = path_finder.shortest_path(
        graph,
        "internet",
        "rds",
    )

    assert path == [
        "internet",
        "alb",
        "ec2",
        "rds",
    ]


def test_path_finder_uses_reverse_protected_by_security_propagation():
    from app.engines.graph.models import GraphEdge, GraphNode, KnowledgeGraph

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

    path = PathFinder().shortest_path(
        graph,
        "security_group",
        "instance",
    )

    assert path == [
        "security_group",
        "instance",
    ]

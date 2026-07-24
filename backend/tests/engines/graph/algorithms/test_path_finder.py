from app.engines.graph.algorithms import PathFinder
from app.engines.graph.models import GraphEdge, GraphNode, KnowledgeGraph


def test_shortest_path_returns_expected_path():
    graph = KnowledgeGraph(
        nodes=[
            GraphNode("internet", "Internet", "external"),
            GraphNode("alb", "ALB", "aws_lb"),
            GraphNode("ec2", "EC2", "aws_instance"),
            GraphNode("rds", "RDS", "aws_db_instance"),
        ],
        edges=[
            GraphEdge("internet", "alb", "connects"),
            GraphEdge("alb", "ec2", "connects"),
            GraphEdge("ec2", "rds", "connects"),
        ],
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

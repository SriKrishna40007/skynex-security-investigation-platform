from app.engines.graph.algorithms import GraphTraversal
from app.engines.graph.models import GraphEdge, GraphNode, KnowledgeGraph


def test_reachable_nodes_returns_all_reachable_nodes():
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

    traversal = GraphTraversal()

    reachable = traversal.reachable_nodes(graph, "internet")

    assert reachable == {
        "internet",
        "alb",
        "ec2",
        "rds",
    }

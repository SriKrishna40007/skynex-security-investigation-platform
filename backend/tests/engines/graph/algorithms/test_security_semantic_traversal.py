from app.engines.graph.algorithms import (
    BreadthFirstTraversal,
    PathFinder,
)
from app.engines.graph.models import (
    GraphEdge,
    GraphNode,
    KnowledgeGraph,
)


def _build_semantic_graph() -> KnowledgeGraph:
    graph = KnowledgeGraph()

    for node_id in (
        "internet",
        "service",
        "database",
        "metadata",
    ):
        graph.add_node(
            GraphNode(
                id=node_id,
                label=node_id,
                resource_type="test",
            )
        )

    graph.add_edge(
        GraphEdge(
            source="internet",
            target="service",
            relationship_type="references",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="service",
            target="database",
            relationship_type="allows_action",
        )
    )

    graph.add_edge(
        GraphEdge(
            source="service",
            target="metadata",
            relationship_type="descriptive_metadata",
        )
    )

    return graph


def test_path_finder_follows_security_traversable_edges():
    graph = _build_semantic_graph()

    path = PathFinder().shortest_path(
        graph,
        "internet",
        "database",
    )

    assert path == [
        "internet",
        "service",
        "database",
    ]


def test_path_finder_rejects_non_security_edge():
    graph = _build_semantic_graph()

    path = PathFinder().shortest_path(
        graph,
        "internet",
        "metadata",
    )

    assert path == []


def test_breadth_first_traversal_follows_security_edges():
    graph = _build_semantic_graph()

    reachable = BreadthFirstTraversal().traverse(
        graph,
        "internet",
    )

    assert reachable == [
        "internet",
        "service",
        "database",
    ]


def test_breadth_first_traversal_rejects_non_security_edge():
    graph = _build_semantic_graph()

    reachable = BreadthFirstTraversal().traverse(
        graph,
        "service",
    )

    assert "database" in reachable
    assert "metadata" not in reachable

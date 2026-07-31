from app.engines.attack_path.policies import (
    AttackPathSemanticRiskPolicy,
)
from app.engines.graph.models import GraphEdge, KnowledgeGraph


def _graph_with_edge(
    relationship_type: str,
) -> KnowledgeGraph:
    graph = KnowledgeGraph()

    graph.add_edge(
        GraphEdge(
            source="source",
            target="target",
            relationship_type=relationship_type,
        )
    )

    return graph


def test_assume_role_relationship_is_high_risk():
    policy = AttackPathSemanticRiskPolicy()

    assessment = policy.evaluate(
        _graph_with_edge("allows_assume_role"),
        ["source", "target"],
    )

    assert assessment.severity == "HIGH"


def test_action_authorization_is_medium_risk():
    policy = AttackPathSemanticRiskPolicy()

    assessment = policy.evaluate(
        _graph_with_edge("allows_action"),
        ["source", "target"],
    )

    assert assessment.severity == "MEDIUM"


def test_connectivity_path_is_medium_risk():
    policy = AttackPathSemanticRiskPolicy()

    assessment = policy.evaluate(
        _graph_with_edge("connects"),
        ["source", "target"],
    )

    assert assessment.severity == "MEDIUM"


def test_missing_path_is_low_risk():
    policy = AttackPathSemanticRiskPolicy()

    assessment = policy.evaluate(
        KnowledgeGraph(),
        [],
    )

    assert assessment.severity == "LOW"


def test_unknown_relationship_does_not_create_elevated_semantic_risk():
    policy = AttackPathSemanticRiskPolicy()

    assessment = policy.evaluate(
        _graph_with_edge("descriptive_metadata"),
        ["source", "target"],
    )

    assert assessment.severity == "LOW"


def test_three_hop_connectivity_path_remains_high_risk():
    """
    Ordinary connectivity depth must not become CRITICAL solely because
    several traversable relationships are chained together.

    CRITICAL severity is reserved for stronger semantic evidence.
    """

    graph = KnowledgeGraph()

    graph.add_edge(
        GraphEdge(
            source="internet",
            target="gateway",
            relationship_type="connects",
        )
    )
    graph.add_edge(
        GraphEdge(
            source="gateway",
            target="service",
            relationship_type="connects",
        )
    )
    graph.add_edge(
        GraphEdge(
            source="service",
            target="database",
            relationship_type="connects",
        )
    )

    assessment = AttackPathSemanticRiskPolicy().evaluate(
        graph,
        [
            "internet",
            "gateway",
            "service",
            "database",
        ],
    )

    assert assessment.severity == "HIGH"

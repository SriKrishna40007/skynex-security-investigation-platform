from app.application.orchestrators import InvestigationOrchestrator
from app.application.pipeline.investigation_pipeline import InvestigationPipeline


def _authorization_policy() -> dict:
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": ("arn:aws:iam::123456789012:role/ProductionAdmin"),
            },
            {
                "Effect": "Allow",
                "Action": "secretsmanager:GetSecretValue",
                "Resource": (
                    "arn:aws:secretsmanager:ap-south-1:"
                    "123456789012:secret:production/database"
                ),
            },
        ],
    }


def test_iam_policy_builds_canonical_authorization_topology():
    orchestrator = InvestigationOrchestrator()

    investigation = orchestrator.investigate_iam_policy(_authorization_policy())

    resource_ids = {resource.id for resource in investigation.resources}

    assert "aws.iam_policy.iam-policy" in resource_ids
    assert "arn:aws:iam::123456789012:role/ProductionAdmin" in resource_ids
    assert (
        "arn:aws:secretsmanager:ap-south-1:"
        "123456789012:secret:production/database" in resource_ids
    )

    relationships = {
        (
            relationship.source_id,
            relationship.target_id,
            relationship.relationship_type,
        )
        for relationship in investigation.relationships
    }

    assert (
        "aws.iam_policy.iam-policy",
        "arn:aws:iam::123456789012:role/ProductionAdmin",
        "allows_assume_role",
    ) in relationships

    assert (
        "aws.iam_policy.iam-policy",
        ("arn:aws:secretsmanager:ap-south-1:123456789012:secret:production/database"),
        "allows_action",
    ) in relationships


def test_iam_authorization_topology_builds_knowledge_graph():
    orchestrator = InvestigationOrchestrator()
    pipeline = InvestigationPipeline()

    investigation = orchestrator.investigate_iam_policy(_authorization_policy())

    result = pipeline.execute(investigation)

    assert "knowledge_graph" in result.analysis

    graph = result.analysis["knowledge_graph"]

    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2

    assert graph.get_node("arn:aws:iam::123456789012:role/ProductionAdmin") is not None


def test_deny_policy_does_not_create_authorization_relationship():
    policy = {
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Deny",
            "Action": "sts:AssumeRole",
            "Resource": ("arn:aws:iam::123456789012:role/ProductionAdmin"),
        },
    }

    investigation = InvestigationOrchestrator().investigate_iam_policy(policy)

    assert investigation.relationships == []


def test_wildcard_resource_does_not_create_fake_topology():
    policy = {
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*",
        },
    }

    investigation = InvestigationOrchestrator().investigate_iam_policy(policy)

    assert all(resource.id != "*" for resource in investigation.resources)

    assert investigation.relationships == []


def test_iam_assume_role_authorization_is_security_attack_path():
    orchestrator = InvestigationOrchestrator()
    pipeline = InvestigationPipeline()

    investigation = orchestrator.investigate_iam_policy(_authorization_policy())

    result = pipeline.execute(
        investigation,
        source="aws.iam_policy.iam-policy",
        target=("arn:aws:iam::123456789012:role/ProductionAdmin"),
    )

    attack_path = result.analysis["attack_path"]

    assert attack_path.exists is True
    assert attack_path.source == "aws.iam_policy.iam-policy"
    assert attack_path.target == ("arn:aws:iam::123456789012:role/ProductionAdmin")
    assert attack_path.nodes == [
        "aws.iam_policy.iam-policy",
        ("arn:aws:iam::123456789012:role/ProductionAdmin"),
    ]
    assert attack_path.hop_count == 1


def test_iam_action_authorization_is_security_attack_path():
    orchestrator = InvestigationOrchestrator()
    pipeline = InvestigationPipeline()

    investigation = orchestrator.investigate_iam_policy(_authorization_policy())

    secret_arn = (
        "arn:aws:secretsmanager:ap-south-1:123456789012:secret:production/database"
    )

    result = pipeline.execute(
        investigation,
        source="aws.iam_policy.iam-policy",
        target=secret_arn,
    )

    attack_path = result.analysis["attack_path"]

    assert attack_path.exists is True
    assert attack_path.nodes == [
        "aws.iam_policy.iam-policy",
        secret_arn,
    ]
    assert attack_path.hop_count == 1


def test_iam_topology_does_not_fabricate_role_to_secret_attack_path():
    orchestrator = InvestigationOrchestrator()
    pipeline = InvestigationPipeline()

    investigation = orchestrator.investigate_iam_policy(_authorization_policy())

    role_arn = "arn:aws:iam::123456789012:role/ProductionAdmin"

    secret_arn = (
        "arn:aws:secretsmanager:ap-south-1:123456789012:secret:production/database"
    )

    result = pipeline.execute(
        investigation,
        source=role_arn,
        target=secret_arn,
    )

    attack_path = result.analysis["attack_path"]

    assert attack_path.exists is False
    assert attack_path.nodes == []
    assert attack_path.hop_count == 0

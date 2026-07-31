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


def test_iam_policy_authorization_exposure_has_evidence_aware_blast_radius():
    """
    The canonical IAM policy node represents authorization evidence.

    Traversing from this node describes resources reachable through permissions
    granted by the policy. It must not be interpreted as proof that a human or
    workload identity has been compromised.
    """

    orchestrator = InvestigationOrchestrator()
    pipeline = InvestigationPipeline()

    investigation = orchestrator.investigate_iam_policy(_authorization_policy())

    policy_id = "aws.iam_policy.iam-policy"
    role_arn = "arn:aws:iam::123456789012:role/ProductionAdmin"
    secret_arn = (
        "arn:aws:secretsmanager:ap-south-1:123456789012:secret:production/database"
    )

    result = pipeline.execute(
        investigation,
        compromised_resource=policy_id,
    )

    assert result.analysis["blast_radius"] == [
        policy_id,
        role_arn,
        secret_arn,
    ]

    analysis = result.analysis["blast_radius_analysis"]

    assert analysis.compromised_resource == policy_id
    assert analysis.reachable_resources == (
        policy_id,
        role_arn,
        secret_arn,
    )

    assert analysis.affected_resource_count == 2
    assert analysis.maximum_depth == 1

    impacts = {impact.resource_id: impact for impact in analysis.impacts}

    assert impacts[policy_id].depth == 0
    assert impacts[policy_id].relationship_types == ()

    assert impacts[role_arn].depth == 1
    assert impacts[role_arn].relationship_types == ("allows_assume_role",)

    assert impacts[secret_arn].depth == 1
    assert impacts[secret_arn].relationship_types == ("allows_action",)


def test_iam_role_does_not_inherit_policy_authorization_blast_radius():
    """
    Policy permissions must not be projected onto a role unless canonical
    evidence explicitly connects that role to those permissions.
    """

    orchestrator = InvestigationOrchestrator()
    pipeline = InvestigationPipeline()

    investigation = orchestrator.investigate_iam_policy(_authorization_policy())

    role_arn = "arn:aws:iam::123456789012:role/ProductionAdmin"
    secret_arn = (
        "arn:aws:secretsmanager:ap-south-1:123456789012:secret:production/database"
    )

    result = pipeline.execute(
        investigation,
        compromised_resource=role_arn,
    )

    assert result.analysis["blast_radius"] == [
        role_arn,
    ]

    analysis = result.analysis["blast_radius_analysis"]

    assert analysis.compromised_resource == role_arn
    assert analysis.reachable_resources == (role_arn,)

    assert analysis.affected_resource_count == 0
    assert analysis.maximum_depth == 0

    assert all(impact.resource_id != secret_arn for impact in analysis.impacts)

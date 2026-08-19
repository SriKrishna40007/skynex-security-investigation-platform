from app.domain.models.resource import Resource
from app.engines.correlation.rules.iam_permission_rule import IAMPermissionRule


def test_wildcard_iam_policy_creates_allows_action_relationships():
    resources = [
        Resource(
            id="aws_iam_role_policy.wildcard_policy",
            name="wildcard_policy",
            type="aws_iam_role_policy",
            provider="terraform",
            metadata={
                "policy": '${jsonencode({Statement = [{Effect = "Allow", Action = "*", Resource = "*"}]})}',
            },
        ),
        Resource(
            id="aws_s3_bucket.sensitive_data",
            name="sensitive_data",
            type="aws_s3_bucket",
            provider="terraform",
        ),
    ]

    relationships = IAMPermissionRule().discover(resources)

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_id == (
        "aws_iam_role_policy.wildcard_policy"
    )
    assert relationship.target_id == (
        "aws_s3_bucket.sensitive_data"
    )
    assert relationship.relationship_type == "allows_action"


def test_restricted_iam_policy_does_not_create_wildcard_relationship():
    resources = [
        Resource(
            id="aws_iam_role_policy.restricted",
            name="restricted",
            type="aws_iam_role_policy",
            provider="terraform",
            metadata={
                "policy": '${jsonencode({Statement = [{Effect = "Allow", Action = "s3:GetObject", Resource = "arn:aws:s3:::example/*"}]})}',
            },
        ),
        Resource(
            id="aws_s3_bucket.data",
            name="data",
            type="aws_s3_bucket",
            provider="terraform",
        ),
    ]

    relationships = IAMPermissionRule().discover(resources)

    assert relationships == []

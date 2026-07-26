from app.domain.models.investigation import Investigation
from app.domain.models.resource import Resource
from app.engines.correlation.implementations import TerraformCorrelationEngine


def test_terraform_correlation_engine_discovers_relationships():
    investigation = Investigation()

    investigation.resources = [
        Resource(
            id="aws_instance.web",
            name="web",
            type="aws_instance",
            provider="aws",
            metadata={
                "references": [
                    "aws_security_group.web",
                ]
            },
        ),
        Resource(
            id="aws_security_group.web",
            name="web-sg",
            type="aws_security_group",
            provider="aws",
        ),
    ]

    engine = TerraformCorrelationEngine()

    result = engine.correlate(investigation)

    assert len(result.relationships) == 1

    relationship = result.relationships[0]

    assert relationship.source_id == "aws_instance.web"
    assert relationship.target_id == "aws_security_group.web"
    assert relationship.relationship_type == "references"

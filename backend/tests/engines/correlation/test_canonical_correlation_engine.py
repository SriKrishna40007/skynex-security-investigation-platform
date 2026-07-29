from app.domain.models.investigation import Investigation
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource
from app.engines.correlation.implementations.canonical import (
    CanonicalCorrelationEngine,
)


def test_canonical_correlation_discovers_reference_relationships():
    investigation = Investigation(
        resources=[
            Resource(
                id="internet",
                name="Internet",
                type="external",
                provider="external",
                metadata={
                    "references": ["alb"],
                },
            ),
            Resource(
                id="alb",
                name="Application Load Balancer",
                type="aws_lb",
                provider="aws",
                metadata={
                    "references": ["instance"],
                },
            ),
            Resource(
                id="instance",
                name="Application Instance",
                type="aws_instance",
                provider="aws",
            ),
        ]
    )

    result = CanonicalCorrelationEngine().correlate(investigation)

    assert len(result.relationships) == 2

    assert (
        result.relationships[0].source_id,
        result.relationships[0].target_id,
    ) == ("internet", "alb")

    assert (
        result.relationships[1].source_id,
        result.relationships[1].target_id,
    ) == ("alb", "instance")


def test_canonical_correlation_preserves_existing_relationships():
    existing = Relationship(
        source_id="identity",
        target_id="policy",
        relationship_type="attached_to",
        metadata={
            "source": "iam",
        },
    )

    investigation = Investigation(
        resources=[
            Resource(
                id="identity",
                name="Application Role",
                type="iam_role",
                provider="aws",
            ),
            Resource(
                id="policy",
                name="Application Policy",
                type="iam_policy",
                provider="aws",
            ),
        ],
        relationships=[existing],
    )

    result = CanonicalCorrelationEngine().correlate(investigation)

    assert result.relationships == [existing]


def test_canonical_correlation_deduplicates_discovered_relationships():
    investigation = Investigation(
        resources=[
            Resource(
                id="service",
                name="Service",
                type="service",
                provider="aws",
                metadata={
                    "references": [
                        "database",
                        "database",
                    ],
                },
            ),
            Resource(
                id="database",
                name="Database",
                type="database",
                provider="aws",
            ),
        ]
    )

    result = CanonicalCorrelationEngine().correlate(investigation)

    assert len(result.relationships) == 1
    assert result.relationships[0].source_id == "service"
    assert result.relationships[0].target_id == "database"

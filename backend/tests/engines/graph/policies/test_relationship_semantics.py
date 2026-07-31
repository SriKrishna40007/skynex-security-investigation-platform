from app.engines.graph.policies import RelationshipSemantics


def test_infrastructure_relationships_are_security_traversable():
    relationship_types = {
        "references",
        "belongs_to",
        "deployed_in",
        "protected_by",
        "routed_by",
        "attached_to",
        "uses",
    }

    for relationship_type in relationship_types:
        assert RelationshipSemantics.is_security_traversable(relationship_type)


def test_iam_authorization_relationships_are_security_traversable():
    assert RelationshipSemantics.is_security_traversable("allows_assume_role")
    assert RelationshipSemantics.is_security_traversable("allows_action")


def test_unknown_relationship_is_not_security_traversable():
    assert not RelationshipSemantics.is_security_traversable("descriptive_metadata")


def test_policy_is_provider_neutral():
    traversable = RelationshipSemantics.SECURITY_TRAVERSABLE_TYPES

    assert all("aws" not in relationship for relationship in traversable)
    assert all("azure" not in relationship for relationship in traversable)
    assert all("terraform" not in relationship for relationship in traversable)


def test_connects_relationship_is_security_traversable():
    assert RelationshipSemantics.is_security_traversable("connects")

from sqlalchemy import inspect

from app.models import InvestigationRecord, User


def test_investigation_record_uses_expected_table():
    assert InvestigationRecord.__tablename__ == "investigations"


def test_investigation_record_has_ownership_foreign_key():
    mapper = inspect(InvestigationRecord)

    owner_id = mapper.columns["owner_id"]

    foreign_keys = list(owner_id.foreign_keys)

    assert len(foreign_keys) == 1
    assert foreign_keys[0].target_fullname == "users.id"


def test_investigation_record_exposes_persistence_fields():
    mapper = inspect(InvestigationRecord)

    expected = {
        "id",
        "owner_id",
        "investigation_type",
        "status",
        "risk_score",
        "severity",
        "summary",
        "result",
        "created_at",
        "updated_at",
    }

    assert expected.issubset(set(mapper.columns.keys()))


def test_investigation_record_owner_relationship():
    mapper = inspect(InvestigationRecord)

    assert "owner" in mapper.relationships
    assert mapper.relationships["owner"].mapper.class_ is User


def test_user_exposes_investigation_relationship():
    mapper = inspect(User)

    assert "investigations" in mapper.relationships
    assert mapper.relationships["investigations"].mapper.class_ is InvestigationRecord


def test_investigation_defaults_are_persistence_defaults():
    mapper = inspect(InvestigationRecord)

    assert mapper.columns["status"].default.arg == "completed"
    assert mapper.columns["risk_score"].default.arg == 0.0
    assert mapper.columns["severity"].default.arg == "LOW"

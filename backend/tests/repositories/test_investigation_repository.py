from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models import InvestigationRecord, Role, User
from app.repositories import InvestigationRepository


def _database() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    return Session(engine)


def _user(
    db: Session,
    *,
    email: str,
) -> User:
    role = db.query(Role).filter_by(name="viewer").first()

    if role is None:
        role = Role(
            name="viewer",
            description="Viewer",
        )
        db.add(role)
        db.flush()

    user = User(
        full_name="SKYNEX User",
        email=email,
        password_hash="not-a-real-password-hash",
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def _create_record(
    repository: InvestigationRepository,
    *,
    owner_id: str,
    summary: str = "Security investigation",
) -> InvestigationRecord:
    return repository.create(
        owner_id=owner_id,
        investigation_type="terraform",
        status="completed",
        risk_score=55.0,
        severity="MEDIUM",
        summary=summary,
        result={
            "risk": {
                "score": 55,
                "severity": "MEDIUM",
            }
        },
    )


def test_repository_creates_owned_investigation():
    db = _database()

    try:
        user = _user(
            db,
            email="owner@example.com",
        )

        repository = InvestigationRepository(db)

        record = _create_record(
            repository,
            owner_id=user.id,
        )

        assert record.id
        assert record.owner_id == user.id
        assert record.investigation_type == "terraform"
        assert record.status == "completed"
        assert record.risk_score == 55.0
        assert record.severity == "MEDIUM"
    finally:
        db.close()


def test_repository_gets_investigation_by_id():
    db = _database()

    try:
        user = _user(
            db,
            email="lookup@example.com",
        )

        repository = InvestigationRepository(db)

        created = _create_record(
            repository,
            owner_id=user.id,
        )

        loaded = repository.get_by_id(created.id)

        assert loaded is not None
        assert loaded.id == created.id
    finally:
        db.close()


def test_repository_get_owned_by_id_accepts_owner():
    db = _database()

    try:
        user = _user(
            db,
            email="correct-owner@example.com",
        )

        repository = InvestigationRepository(db)

        created = _create_record(
            repository,
            owner_id=user.id,
        )

        loaded = repository.get_owned_by_id(
            investigation_id=created.id,
            owner_id=user.id,
        )

        assert loaded is not None
        assert loaded.owner_id == user.id
    finally:
        db.close()


def test_repository_get_owned_by_id_rejects_other_user():
    db = _database()

    try:
        owner = _user(
            db,
            email="owner-two@example.com",
        )

        other_user = _user(
            db,
            email="other-user@example.com",
        )

        repository = InvestigationRepository(db)

        created = _create_record(
            repository,
            owner_id=owner.id,
        )

        loaded = repository.get_owned_by_id(
            investigation_id=created.id,
            owner_id=other_user.id,
        )

        assert loaded is None
    finally:
        db.close()


def test_repository_lists_only_owner_investigations():
    db = _database()

    try:
        owner = _user(
            db,
            email="list-owner@example.com",
        )

        other_user = _user(
            db,
            email="list-other@example.com",
        )

        repository = InvestigationRepository(db)

        _create_record(
            repository,
            owner_id=owner.id,
            summary="Owner investigation one",
        )

        _create_record(
            repository,
            owner_id=owner.id,
            summary="Owner investigation two",
        )

        _create_record(
            repository,
            owner_id=other_user.id,
            summary="Other investigation",
        )

        records = repository.list_for_owner(owner.id)

        assert len(records) == 2

        assert all(record.owner_id == owner.id for record in records)

        assert {record.summary for record in records} == {
            "Owner investigation one",
            "Owner investigation two",
        }
    finally:
        db.close()


def test_repository_persists_serialized_result():
    db = _database()

    try:
        user = _user(
            db,
            email="result-owner@example.com",
        )

        repository = InvestigationRepository(db)

        record = _create_record(
            repository,
            owner_id=user.id,
        )

        loaded = repository.get_by_id(record.id)

        assert loaded is not None
        assert loaded.result["risk"]["score"] == 55
        assert loaded.result["risk"]["severity"] == "MEDIUM"
    finally:
        db.close()


def test_delete_returns_true_when_record_exists():
    db = Mock()

    record = Mock()

    query = db.query.return_value
    query.filter.return_value.first.return_value = record

    repository = InvestigationRepository(db)

    result = repository.delete(
        owner_id="owner-1",
        investigation_id="investigation-1",
    )

    assert result is True

    db.delete.assert_called_once_with(record)
    db.commit.assert_called_once()


def test_delete_returns_false_when_record_missing():
    db = Mock()

    query = db.query.return_value
    query.filter.return_value.first.return_value = None

    repository = InvestigationRepository(db)

    result = repository.delete(
        owner_id="owner-1",
        investigation_id="missing",
    )

    assert result is False

    db.delete.assert_not_called()
    db.commit.assert_not_called()

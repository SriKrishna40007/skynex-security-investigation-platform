import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.models import Role, User


TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


@pytest.fixture()
def db() -> Session:
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db: Session) -> TestClient:
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def roles(db: Session) -> dict[str, Role]:
    role_names = ("viewer", "analyst", "admin")

    created_roles = {}

    for name in role_names:
        role = Role(
            id=str(uuid.uuid4()),
            name=name,
            description=f"Test {name} role",
        )
        db.add(role)
        created_roles[name] = role

    db.commit()

    return created_roles


@pytest.fixture()
def test_user(db: Session, roles: dict[str, Role]) -> User:
    user = User(
        id=str(uuid.uuid4()),
        full_name="Test Analyst",
        email="test@example.com",
        password_hash=hash_password("TestPassword123!"),
        is_active=True,
        role=roles["viewer"],
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture()
def admin_user(db: Session, roles: dict[str, Role]) -> User:
    user = User(
        id=str(uuid.uuid4()),
        full_name="Test Administrator",
        email="admin@example.com",
        password_hash=hash_password("AdminPassword123!"),
        is_active=True,
        role=roles["admin"],
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

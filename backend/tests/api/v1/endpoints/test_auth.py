from sqlalchemy import select

from app.models import Session as UserSession


def login(client, email: str, password: str) -> dict:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()


def test_register_creates_user(client, roles):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "New Test User",
            "email": "new@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["email"] == "new@example.com"
    assert body["full_name"] == "New Test User"
    assert body["is_active"] is True
    assert "password" not in body
    assert "password_hash" not in body


def test_register_rejects_duplicate_email(client, test_user):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Duplicate User",
            "email": test_user.email,
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "A user with this email already exists."
    )


def test_invalid_login_returns_401(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_valid_login_creates_session(client, db, test_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["session_id"]

    session = db.scalar(
        select(UserSession).where(
            UserSession.id == body["session_id"]
        )
    )

    assert session is not None
    assert session.user_id == test_user.id
    assert session.is_revoked is False


def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_me_returns_authenticated_user(client, test_user):
    tokens = login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == test_user.id
    assert body["email"] == test_user.email
    assert body["full_name"] == test_user.full_name
    assert body["is_active"] is True


def test_invalid_access_token_is_rejected(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer definitely-invalid-token",
        },
    )

    assert response.status_code == 401


def test_viewer_cannot_access_admin_endpoint(client, test_user):
    tokens = login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    response = client.get(
        "/api/v1/auth/admin",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied."


def test_admin_can_access_admin_endpoint(client, admin_user):
    tokens = login(
        client,
        admin_user.email,
        "AdminPassword123!",
    )

    response = client.get(
        "/api/v1/auth/admin",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["role"] == "admin"
    assert admin_user.full_name in body["message"]


def test_refresh_rotates_refresh_token(client, test_user):
    tokens = login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert response.status_code == 200

    refreshed = response.json()

    assert refreshed["session_id"] == tokens["session_id"]
    assert refreshed["access_token"]
    assert refreshed["refresh_token"]

    assert refreshed["refresh_token"] != tokens["refresh_token"]


def test_old_refresh_token_cannot_be_replayed(client, test_user):
    tokens = login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    first_refresh = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert first_refresh.status_code == 200

    replay = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert replay.status_code == 401


def test_logout_revokes_refresh_token(client, test_user):
    tokens = login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    logout = client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert logout.status_code == 204

    refresh = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert refresh.status_code == 401


def test_logout_is_idempotent_for_revoked_session(client, test_user):
    tokens = login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    first = client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert first.status_code == 204

    second = client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert second.status_code == 204

from pathlib import Path

from app.models import InvestigationRecord


TERRAFORM_FILE = (
    Path(__file__).resolve().parents[4] / "examples" / "terraform" / "skynex_demo.tf"
)


def _login(client, email: str, password: str) -> dict:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    return response.json()


def _create_investigation(client, access_token: str) -> str:
    with TERRAFORM_FILE.open("rb") as terraform_file:
        response = client.post(
            "/api/v1/investigations/terraform",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            data={
                "source": "aws_security_group.web",
                "target": "aws_instance.web",
            },
            files={
                "terraform_file": (
                    "skynex_demo.tf",
                    terraform_file,
                    "text/plain",
                ),
            },
        )

    assert response.status_code == 200

    investigation_id = response.json()["id"]
    assert investigation_id

    return investigation_id


def test_authenticated_history_returns_only_owned_investigations(
    client,
    db,
    admin_user,
    investigator_user,
):
    # ---------------------------------------------------------
    # 1. USER A LOGIN
    # ---------------------------------------------------------
    owner_tokens = _login(
        client,
        admin_user.email,
        "AdminPassword123!",
    )

    # ---------------------------------------------------------
    # 2. USER A CREATES INVESTIGATION
    # ---------------------------------------------------------
    owner_investigation_id = _create_investigation(
        client,
        owner_tokens["access_token"],
    )

    # ---------------------------------------------------------
    # 3. USER B LOGIN
    # ---------------------------------------------------------
    other_tokens = _login(
        client,
        investigator_user.email,
        "InvestigatorPassword123!",
    )

    # ---------------------------------------------------------
    # 4. USER B CREATES OWN INVESTIGATION
    # ---------------------------------------------------------
    other_investigation_id = _create_investigation(
        client,
        other_tokens["access_token"],
    )

    # ---------------------------------------------------------
    # 5. USER B REQUESTS HISTORY
    # ---------------------------------------------------------
    response = client.get(
        "/api/v1/investigations",
        headers={
            "Authorization": f"Bearer {other_tokens['access_token']}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["page"] == 1
    assert body["size"] == 20
    assert body["total"] == 1
    assert body["pages"] == 1
    assert len(body["items"]) == 1

    returned_ids = {item["id"] for item in body["items"]}

    assert other_investigation_id in returned_ids
    assert owner_investigation_id not in returned_ids

    # ---------------------------------------------------------
    # 6. DATABASE OWNERSHIP ASSERTION
    # ---------------------------------------------------------
    owner_record = (
        db.query(InvestigationRecord)
        .filter(InvestigationRecord.id == owner_investigation_id)
        .first()
    )

    other_record = (
        db.query(InvestigationRecord)
        .filter(InvestigationRecord.id == other_investigation_id)
        .first()
    )

    assert owner_record is not None
    assert other_record is not None

    assert owner_record.owner_id == admin_user.id
    assert other_record.owner_id == investigator_user.id


def test_investigation_history_requires_authentication(client):
    response = client.get("/api/v1/investigations")

    assert response.status_code == 401


def test_investigation_history_filters_owned_records(
    client,
    admin_user,
):
    tokens = _login(
        client,
        admin_user.email,
        "AdminPassword123!",
    )

    _create_investigation(
        client,
        tokens["access_token"],
    )

    response = client.get(
        "/api/v1/investigations",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        params={
            "investigation_type": "terraform",
            "severity": "LOW",
            "page": 1,
            "size": 20,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert body["pages"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["investigation_type"] == "terraform"
    assert body["items"][0]["severity"] == "LOW"

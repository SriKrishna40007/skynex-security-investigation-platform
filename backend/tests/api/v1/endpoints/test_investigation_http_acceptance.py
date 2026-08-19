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


def test_authenticated_terraform_investigation_full_http_flow(
    client,
    db,
    admin_user,
):
    # ---------------------------------------------------------
    # 1. REAL LOGIN
    # ---------------------------------------------------------
    tokens = _login(
        client,
        admin_user.email,
        "AdminPassword123!",
    )

    assert tokens["token_type"] == "bearer"
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["session_id"]

    # ---------------------------------------------------------
    # 2. REAL AUTHENTICATED INVESTIGATION REQUEST
    # ---------------------------------------------------------
    with TERRAFORM_FILE.open("rb") as terraform_file:
        response = client.post(
            "/api/v1/investigations/terraform",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}",
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

    # ---------------------------------------------------------
    # 3. HTTP CONTRACT
    # ---------------------------------------------------------
    assert response.status_code == 200

    body = response.json()

    assert body["id"]
    assert body["attack_path"] == [
        "aws_security_group.web",
        "aws_instance.web",
    ]

    assert body["attack_path_analysis"]["exists"] is True
    assert body["attack_path_analysis"]["source"] == ("aws_security_group.web")
    assert body["attack_path_analysis"]["target"] == ("aws_instance.web")
    assert body["attack_path_analysis"]["hop_count"] == 1

    assert body["blast_radius"]
    assert body["blast_radius_analysis"]["affected_resource_count"] == 3
    assert body["blast_radius_analysis"]["maximum_depth"] == 2

    assert body["candidates"]
    assert body["candidate_context"]
    assert body["candidate_impact"]

    assert body["risk"] is not None
    assert body["reasoning"] is not None

    # ---------------------------------------------------------
    # 4. PERSISTENCE CONTRACT
    # ---------------------------------------------------------
    record = (
        db.query(InvestigationRecord)
        .filter(InvestigationRecord.id == body["id"])
        .first()
    )

    assert record is not None
    assert record.owner_id == admin_user.id
    assert record.investigation_type == "terraform"


def test_investigation_isolation_between_users(
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
    with TERRAFORM_FILE.open("rb") as terraform_file:
        create_response = client.post(
            "/api/v1/investigations/terraform",
            headers={
                "Authorization": f"Bearer {owner_tokens['access_token']}",
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

    assert create_response.status_code == 200

    investigation_id = create_response.json()["id"]
    assert investigation_id

    # ---------------------------------------------------------
    # 3. VERIFY DATABASE OWNERSHIP
    # ---------------------------------------------------------
    record = (
        db.query(InvestigationRecord)
        .filter(InvestigationRecord.id == investigation_id)
        .first()
    )

    assert record is not None
    assert record.owner_id == admin_user.id

    # ---------------------------------------------------------
    # 4. USER B LOGIN
    # ---------------------------------------------------------
    viewer_tokens = _login(
        client,
        investigator_user.email,
        "InvestigatorPassword123!",
    )

    viewer_headers = {
        "Authorization": f"Bearer {viewer_tokens['access_token']}",
    }

    # ---------------------------------------------------------
    # 5. USER B CANNOT READ USER A'S INVESTIGATION
    # ---------------------------------------------------------
    read_response = client.get(
        f"/api/v1/investigations/{investigation_id}",
        headers=viewer_headers,
    )

    assert read_response.status_code == 404

    # ---------------------------------------------------------
    # 6. USER B CANNOT EXPORT USER A'S INVESTIGATION
    # ---------------------------------------------------------
    export_response = client.get(
        f"/api/v1/investigations/{investigation_id}/export",
        headers=viewer_headers,
    )

    assert export_response.status_code == 404

    # ---------------------------------------------------------
    # 7. USER B CANNOT DELETE USER A'S INVESTIGATION
    # ---------------------------------------------------------
    delete_response = client.delete(
        f"/api/v1/investigations/{investigation_id}",
        headers=viewer_headers,
    )

    assert delete_response.status_code == 404

    # ---------------------------------------------------------
    # 8. USER A STILL OWNS THE RECORD
    # ---------------------------------------------------------
    db.expire_all()

    record = (
        db.query(InvestigationRecord)
        .filter(InvestigationRecord.id == investigation_id)
        .first()
    )

    assert record is not None
    assert record.owner_id == admin_user.id


def test_invalid_terraform_syntax_returns_400(
    client,
    admin_user,
):
    tokens = _login(
        client,
        admin_user.email,
        "AdminPassword123!",
    )

    fixture = (
        Path(__file__).resolve().parents[4]
        / "tests"
        / "fixtures"
        / "v1"
        / "10_invalid_syntax.tf"
    )

    with fixture.open("rb") as terraform_file:
        response = client.post(
            "/api/v1/investigations/terraform",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}",
            },
            data={
                "source": "aws_instance.invalid",
                "target": "aws_s3_bucket.invalid",
            },
            files={
                "terraform_file": (
                    fixture.name,
                    terraform_file,
                    "text/plain",
                ),
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid Terraform configuration."


def test_duplicate_terraform_resource_returns_400(
    client,
    admin_user,
):
    tokens = _login(
        client,
        admin_user.email,
        "AdminPassword123!",
    )

    fixture = (
        Path(__file__).resolve().parents[4]
        / "tests"
        / "fixtures"
        / "v1"
        / "13_duplicate_resources.tf"
    )

    with fixture.open("rb") as terraform_file:
        response = client.post(
            "/api/v1/investigations/terraform",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}",
            },
            data={
                "source": "aws_instance.duplicate",
                "target": "aws_s3_bucket.duplicate",
            },
            files={
                "terraform_file": (
                    fixture.name,
                    terraform_file,
                    "text/plain",
                ),
            },
        )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Duplicate Terraform resource address: "
        "aws_s3_bucket.dup_bucket"
    )

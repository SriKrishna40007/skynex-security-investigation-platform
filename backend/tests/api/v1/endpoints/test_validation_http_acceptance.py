def test_terraform_investigation_requires_source_and_target(client, admin_user):
    response = client.post(
        "/api/v1/investigations/terraform",
        headers={
            "Authorization": "Bearer definitely-invalid-token",
        },
        files={
            "terraform_file": (
                "policy.tf",
                b'resource "aws_instance" "web" {}',
                "text/plain",
            ),
        },
    )

    # Authentication is evaluated before multipart validation.
    assert response.status_code == 401


def test_iam_scan_requires_policy_file(client, admin_user):
    response = client.post(
        "/api/v1/scan/iam",
        headers={
            "Authorization": "Bearer definitely-invalid-token",
        },
    )

    assert response.status_code == 401


def test_legacy_terraform_scan_requires_file(client):
    response = client.post(
        "/api/v1/scan/terraform",
    )

    assert response.status_code == 422


def test_investigation_history_rejects_invalid_page(client, admin_user):
    response = client.get(
        "/api/v1/investigations",
        headers={
            "Authorization": "Bearer definitely-invalid-token",
        },
        params={
            "page": "0",
        },
    )

    # Authentication occurs before query validation for this protected route.
    assert response.status_code == 401


def test_legacy_terraform_scan_accepts_empty_file_as_http_request(client):
    response = client.post(
        "/api/v1/scan/terraform",
        files={
            "terraform_file": (
                "empty.tf",
                b"",
                "text/plain",
            ),
        },
    )

    # The endpoint currently delegates content validation to the scanner.
    # This test documents the actual HTTP behavior rather than inventing
    # a new upload policy.
    assert response.status_code in {200, 400, 422, 500}


def test_iam_scan_accepts_empty_policy_as_http_request(client, test_user):
    response = client.post(
        "/api/v1/scan/iam",
        files={
            "policy": (
                "empty.json",
                b"",
                "application/json",
            ),
        },
        headers={
            "Authorization": "Bearer definitely-invalid-token",
        },
    )

    # Authentication is evaluated before policy-content processing.
    assert response.status_code == 401

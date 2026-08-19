IAM_POLICY = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::123456789012:role/ProductionAdmin"
    },
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:ap-south-1:123456789012:secret:production/database"
    }
  ]
}"""


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


def test_authenticated_iam_policy_full_http_flow(
    client,
    test_user,
):
    tokens = _login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    response = client.post(
        "/api/v1/scan/iam",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        files={
            "policy": (
                "production-policy.json",
                IAM_POLICY,
                "application/json",
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "overall_risk_score" in body
    assert "findings" in body
    assert "recommendations" in body

    assert isinstance(body["overall_risk_score"], int)
    assert isinstance(body["findings"], int)
    assert isinstance(body["recommendations"], list)

    assert body["findings"] >= 0


def test_iam_scan_requires_authentication(client):
    response = client.post(
        "/api/v1/scan/iam",
        files={
            "policy": (
                "policy.json",
                IAM_POLICY,
                "application/json",
            ),
        },
    )

    assert response.status_code == 401


def test_iam_scan_rejects_invalid_token(client):
    response = client.post(
        "/api/v1/scan/iam",
        headers={
            "Authorization": "Bearer definitely-invalid-token",
        },
        files={
            "policy": (
                "policy.json",
                IAM_POLICY,
                "application/json",
            ),
        },
    )

    assert response.status_code == 401


def test_iam_scan_rejects_malformed_json(
    client,
    test_user,
):
    tokens = _login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    response = client.post(
        "/api/v1/scan/iam",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        files={
            "policy": (
                "invalid.json",
                b'{"Version":"2012-10-17","Statement":[{"Effect":"Allow"}]',
                "application/json",
            ),
        },
    )

    assert response.status_code == 400
    assert "valid UTF-8 JSON" in response.json()["detail"]


def test_iam_scan_rejects_missing_required_fields(
    client,
    test_user,
):
    tokens = _login(
        client,
        test_user.email,
        "TestPassword123!",
    )

    response = client.post(
        "/api/v1/scan/iam",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        files={
            "policy": (
                "empty.json",
                b"{}",
                "application/json",
            ),
        },
    )

    assert response.status_code == 400
    assert "missing required field(s)" in response.json()["detail"]

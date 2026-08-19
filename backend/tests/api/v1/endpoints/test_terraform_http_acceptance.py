from pathlib import Path


TERRAFORM_FILE = (
    Path(__file__).resolve().parents[4] / "examples" / "terraform" / "skynex_demo.tf"
)


def test_legacy_terraform_scan_returns_investigation_report(client):
    with TERRAFORM_FILE.open("rb") as terraform_file:
        response = client.post(
            "/api/v1/scan/terraform",
            files={
                "terraform_file": (
                    "skynex_demo.tf",
                    terraform_file,
                    "text/plain",
                ),
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert "summary" in body
    assert "findings" in body

    assert isinstance(body["summary"], dict)
    assert isinstance(body["findings"], list)

    assert body["summary"]["scanner"] == "terraform"
    assert body["summary"]["total_findings"] == len(body["findings"])

    for finding in body["findings"]:
        assert finding["scanner"] == "terraform"
        assert finding["severity"] in {"HIGH", "MEDIUM", "LOW"}
        assert finding["resource"]
        assert finding["rule_id"]

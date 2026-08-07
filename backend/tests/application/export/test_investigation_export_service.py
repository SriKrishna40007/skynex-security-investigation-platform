from unittest.mock import Mock

from app.application.export import InvestigationExportService
from app.schemas.export import InvestigationExportResponse


def _record():
    record = Mock()

    record.id = "inv-001"
    record.investigation_type = "terraform"
    record.status = "completed"
    record.severity = "HIGH"
    record.risk_score = 82.5
    record.summary = "Terraform investigation"
    record.result = {
        "risk": {
            "score": 82,
            "severity": "HIGH",
        }
    }

    return record


def test_export_json():

    service = InvestigationExportService()

    response = service.export(
        _record(),
        "json",
    )

    assert isinstance(
        response,
        InvestigationExportResponse,
    )

    assert response.filename == "inv-001.json"
    assert response.content_type == "application/json"
    assert '"severity": "HIGH"' in response.content


def test_export_markdown():

    service = InvestigationExportService()

    response = service.export(
        _record(),
        "markdown",
    )

    assert response.filename == "inv-001.md"
    assert response.content_type == "text/markdown"

    assert "# Investigation" in response.content
    assert "Terraform investigation" in response.content

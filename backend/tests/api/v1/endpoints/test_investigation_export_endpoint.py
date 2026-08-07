from unittest.mock import Mock

from app.api.v1.endpoints import investigation as endpoint
from app.schemas.export import InvestigationExportResponse


class _User:
    id = "owner-1"


def test_export_investigation_returns_export(monkeypatch):
    record = Mock()

    persistence = Mock()
    persistence.read.return_value = record

    exporter = Mock()
    exporter.export.return_value = InvestigationExportResponse(
        filename="investigation.json",
        content_type="application/json",
        content="{}",
    )

    monkeypatch.setattr(
        endpoint,
        "InvestigationPersistenceService",
        Mock(return_value=persistence),
    )

    monkeypatch.setattr(
        endpoint,
        "InvestigationExportService",
        Mock(return_value=exporter),
    )

    response = endpoint.export_investigation(
        investigation_id="inv-1",
        format="json",
        current_user=_User(),
        db=Mock(),
    )

    assert response.filename == "investigation.json"
    assert response.content_type == "application/json"

    persistence.read.assert_called_once_with(
        owner_id="owner-1",
        investigation_id="inv-1",
    )

    exporter.export.assert_called_once_with(
        record,
        "json",
    )

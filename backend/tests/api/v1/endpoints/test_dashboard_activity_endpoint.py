from datetime import UTC, datetime
from unittest.mock import Mock

from app.api.v1.endpoints import dashboard as endpoint
from app.schemas.dashboard import DashboardActivityResponse


class _User:
    id = "admin-1"


def test_dashboard_activity_returns_service_response(monkeypatch):
    expected = [
        DashboardActivityResponse(
            id="1",
            investigation_type="terraform",
            status="completed",
            severity="HIGH",
            summary="Terraform investigation",
            risk_score=81.5,
            created_at=datetime.now(UTC),
        )
    ]

    service = Mock()
    service.activity.return_value = expected

    monkeypatch.setattr(
        endpoint,
        "DashboardService",
        Mock(return_value=service),
    )

    response = endpoint.dashboard_activity(
        limit=10,
        db=Mock(),
        current_user=_User(),
    )

    service.activity.assert_called_once_with(10)

    assert response == expected

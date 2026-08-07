from unittest.mock import Mock

from app.api.v1.endpoints import dashboard as endpoint
from app.schemas.dashboard import DashboardSummaryResponse


class _User:
    id = "admin-1"


def test_dashboard_summary_returns_service_response(monkeypatch):
    expected = DashboardSummaryResponse(
        total_investigations=15,
        completed=12,
        failed=3,
        critical=1,
        high=2,
        medium=4,
        low=8,
        average_risk_score=64.2,
    )

    service = Mock()
    service.summary.return_value = expected

    monkeypatch.setattr(
        endpoint,
        "DashboardService",
        Mock(return_value=service),
    )

    response = endpoint.dashboard_summary(
        db=Mock(),
        current_user=_User(),
    )

    service.summary.assert_called_once()

    assert response == expected

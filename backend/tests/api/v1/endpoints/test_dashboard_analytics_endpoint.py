from unittest.mock import Mock

from app.api.v1.endpoints import dashboard as endpoint
from app.schemas.dashboard import (
    DashboardAnalyticsResponse,
    InvestigationTypeDistribution,
    SeverityDistribution,
)


class _User:
    id = "admin-1"


def test_dashboard_analytics_returns_service_response(monkeypatch):
    expected = DashboardAnalyticsResponse(
        investigation_trend=[],
        average_risk_trend=[],
        severity_distribution=SeverityDistribution(
            critical=1,
            high=2,
            medium=3,
            low=4,
        ),
        investigation_type_distribution=InvestigationTypeDistribution(
            terraform=6,
            iam=2,
        ),
    )

    service = Mock()
    service.analytics.return_value = expected

    monkeypatch.setattr(
        endpoint,
        "DashboardService",
        Mock(return_value=service),
    )

    response = endpoint.dashboard_analytics(
        db=Mock(),
        current_user=_User(),
    )

    service.analytics.assert_called_once()

    assert response == expected

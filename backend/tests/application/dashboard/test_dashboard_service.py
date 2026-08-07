from datetime import UTC, datetime
from unittest.mock import Mock

from app.application.dashboard import DashboardService
from app.schemas.dashboard import DashboardSummaryResponse


def test_dashboard_service_maps_repository_response():
    repository = Mock()

    repository.summary.return_value = {
        "total_investigations": 25,
        "completed": 20,
        "failed": 5,
        "critical": 2,
        "high": 4,
        "medium": 8,
        "low": 11,
        "average_risk_score": 57.3,
    }

    service = DashboardService(repository)

    response = service.summary()

    assert isinstance(response, DashboardSummaryResponse)
    assert response.total_investigations == 25
    assert response.completed == 20
    assert response.failed == 5
    assert response.critical == 2
    assert response.high == 4
    assert response.medium == 8
    assert response.low == 11
    assert response.average_risk_score == 57.3


class _Record:
    id = "1"
    investigation_type = "terraform"
    status = "completed"
    severity = "HIGH"
    summary = "Terraform investigation"
    risk_score = 78.5
    created_at = datetime.now(UTC)


def test_dashboard_service_returns_activity():
    repository = Mock()

    repository.activity.return_value = [
        _Record(),
    ]

    service = DashboardService(repository)

    response = service.activity()

    assert len(response) == 1
    assert response[0].id == "1"
    assert response[0].investigation_type == "terraform"
    assert response[0].status == "completed"
    assert response[0].severity == "HIGH"
    assert response[0].summary == "Terraform investigation"
    assert response[0].risk_score == 78.5


def test_dashboard_service_returns_analytics():
    repository = Mock()

    repository.analytics.return_value = {
        "investigation_trend": [],
        "average_risk_trend": [],
        "severity_distribution": {
            "critical": 1,
            "high": 2,
            "medium": 3,
            "low": 4,
        },
        "investigation_type_distribution": {
            "terraform": 6,
            "iam": 2,
        },
    }

    service = DashboardService(repository)

    response = service.analytics()

    assert response.severity_distribution.critical == 1
    assert response.severity_distribution.high == 2
    assert response.severity_distribution.medium == 3
    assert response.severity_distribution.low == 4

    assert response.investigation_type_distribution.terraform == 6
    assert response.investigation_type_distribution.iam == 2

    assert response.investigation_trend == []
    assert response.average_risk_trend == []

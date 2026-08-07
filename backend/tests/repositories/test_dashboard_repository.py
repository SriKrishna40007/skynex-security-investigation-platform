from unittest.mock import Mock

from app.repositories.dashboard_repository import DashboardRepository


def test_summary_returns_repository_metrics():
    db = Mock()

    row = Mock(
        total=10,
        completed=8,
        failed=2,
        critical=1,
        high=2,
        medium=3,
        low=4,
        average_risk_score=61.5,
    )

    db.execute.return_value.one.return_value = row

    repository = DashboardRepository(db)

    result = repository.summary()

    assert result["total_investigations"] == 10
    assert result["completed"] == 8
    assert result["failed"] == 2
    assert result["critical"] == 1
    assert result["high"] == 2
    assert result["medium"] == 3
    assert result["low"] == 4
    assert result["average_risk_score"] == 61.5


def test_summary_returns_zero_when_database_is_empty():
    db = Mock()

    row = Mock(
        total=None,
        completed=None,
        failed=None,
        critical=None,
        high=None,
        medium=None,
        low=None,
        average_risk_score=None,
    )

    db.execute.return_value.one.return_value = row

    repository = DashboardRepository(db)

    result = repository.summary()

    assert result == {
        "total_investigations": 0,
        "completed": 0,
        "failed": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "average_risk_score": 0.0,
    }


def test_activity_returns_recent_investigations():
    db = Mock()

    expected = ["record-1", "record-2", "record-3"]

    db.scalars.return_value.all.return_value = expected

    repository = DashboardRepository(db)

    result = repository.activity(limit=3)

    assert result == expected

    db.scalars.assert_called_once()

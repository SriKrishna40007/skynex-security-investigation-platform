from datetime import UTC, datetime

from app.schemas.investigation import (
    InvestigationHistoryResponse,
)


def test_history_response_contract():
    response = InvestigationHistoryResponse(
        id="abc123",
        investigation_type="terraform",
        status="completed",
        severity="HIGH",
        risk_score=82.5,
        summary="Investigation completed.",
        created_at=datetime.now(UTC),
    )

    assert response.id == "abc123"
    assert response.investigation_type == "terraform"
    assert response.status == "completed"
    assert response.severity == "HIGH"
    assert response.risk_score == 82.5

from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import UploadFile

from app.api.v1.endpoints import investigation as endpoint
from app.domain.models.investigation import Investigation
from app.models import InvestigationRecord


class _AuthenticatedUser:
    id = "owner-123"
    full_name = "SKYNEX Analyst"
    email = "analyst@example.com"
    is_active = True


def _investigation() -> Investigation:
    return Investigation(
        risk_score=55.0,
        summary="Persisted SKYNEX investigation.",
    )


@pytest.mark.anyio
async def test_terraform_endpoint_persists_completed_investigation(
    monkeypatch,
):
    investigation = _investigation()

    monkeypatch.setattr(
        endpoint.orchestrator,
        "investigate_terraform",
        AsyncMock(return_value=investigation),
    )

    persisted = Mock(spec=InvestigationRecord)

    persist = Mock(return_value=persisted)

    monkeypatch.setattr(
        endpoint.InvestigationPersistenceService,
        "persist",
        persist,
    )

    db = Mock()

    upload = UploadFile(
        filename="main.tf",
        file=None,
    )

    response = await endpoint.investigate_terraform(
        terraform_file=upload,
        source="external-user",
        target="production-secret",
        current_user=_AuthenticatedUser(),
        db=db,
    )

    persist.assert_called_once()

    call = persist.call_args.kwargs

    assert call["owner_id"] == "owner-123"
    assert call["investigation_type"] == "terraform"
    assert call["investigation"] is investigation
    assert call["response"] is response


@pytest.mark.anyio
async def test_endpoint_returns_public_response_after_persistence(
    monkeypatch,
):
    investigation = _investigation()

    monkeypatch.setattr(
        endpoint.orchestrator,
        "investigate_terraform",
        AsyncMock(return_value=investigation),
    )

    monkeypatch.setattr(
        endpoint.InvestigationPersistenceService,
        "persist",
        Mock(return_value=Mock(spec=InvestigationRecord)),
    )

    response = await endpoint.investigate_terraform(
        terraform_file=UploadFile(
            filename="main.tf",
            file=None,
        ),
        source="external-user",
        target="production-secret",
        current_user=_AuthenticatedUser(),
        db=Mock(),
    )

    assert response.risk_score == 55.0
    assert response.summary == "Persisted SKYNEX investigation."


@pytest.mark.anyio
async def test_failed_analysis_is_not_persisted(
    monkeypatch,
):
    failure = RuntimeError("analysis failed")

    monkeypatch.setattr(
        endpoint.orchestrator,
        "investigate_terraform",
        AsyncMock(side_effect=failure),
    )

    persist = Mock()

    monkeypatch.setattr(
        endpoint.InvestigationPersistenceService,
        "persist",
        persist,
    )

    with pytest.raises(RuntimeError, match="analysis failed"):
        await endpoint.investigate_terraform(
            terraform_file=UploadFile(
                filename="main.tf",
                file=None,
            ),
            source="external-user",
            target="production-secret",
            current_user=_AuthenticatedUser(),
            db=Mock(),
        )

    persist.assert_not_called()

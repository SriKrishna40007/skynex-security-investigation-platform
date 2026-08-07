from unittest.mock import Mock

from app.application.services import InvestigationPersistenceService
from app.domain.models.investigation import Investigation
from app.models import InvestigationRecord
from app.repositories import InvestigationRepository
from app.schemas.investigation import (
    ReasoningResponse,
    InvestigationResponse,
    RiskAssessmentResponse,
)


def _response(
    *,
    risk: RiskAssessmentResponse | None = None,
    reasoning: ReasoningResponse | None = None,
) -> InvestigationResponse:
    return InvestigationResponse(
        attack_path=[],
        blast_radius=[],
        risk_score=55.0,
        summary="SKYNEX investigation",
        risk=risk,
        reasoning=reasoning,
    )


def test_service_persists_completed_investigation():
    repository = Mock(spec=InvestigationRepository)

    expected = Mock(spec=InvestigationRecord)
    repository.create.return_value = expected

    service = InvestigationPersistenceService(
        repository,
    )

    investigation = Investigation(
        risk_score=55.0,
        summary="SKYNEX investigation",
    )

    response = _response(
        risk=RiskAssessmentResponse(
            score=55,
            severity="MEDIUM",
            reasons=[
                "Attack path exists.",
            ],
        )
    )

    result = service.persist(
        owner_id="user-123",
        investigation_type="terraform",
        investigation=investigation,
        response=response,
    )

    assert result is expected

    repository.create.assert_called_once()

    call = repository.create.call_args.kwargs

    assert call["owner_id"] == "user-123"
    assert call["investigation_type"] == "terraform"
    assert call["status"] == "completed"
    assert call["risk_score"] == 55.0
    assert call["severity"] == "MEDIUM"
    assert call["summary"] == "SKYNEX investigation"


def test_service_serializes_public_response_contract():
    repository = Mock(spec=InvestigationRepository)

    repository.create.return_value = Mock(spec=InvestigationRecord)

    service = InvestigationPersistenceService(
        repository,
    )

    investigation = Investigation(
        risk_score=55.0,
        summary="Serializable investigation",
    )

    response = _response(
        risk=RiskAssessmentResponse(
            score=55,
            severity="MEDIUM",
            reasons=[],
        )
    )

    service.persist(
        owner_id="user-123",
        investigation_type="terraform",
        investigation=investigation,
        response=response,
    )

    result = repository.create.call_args.kwargs["result"]

    assert isinstance(result, dict)
    assert result["risk_score"] == 55.0
    assert result["summary"] == "SKYNEX investigation"
    assert result["risk"]["severity"] == "MEDIUM"


def test_service_prefers_canonical_risk_severity():
    repository = Mock(spec=InvestigationRepository)

    repository.create.return_value = Mock(spec=InvestigationRecord)

    service = InvestigationPersistenceService(
        repository,
    )

    service.persist(
        owner_id="owner",
        investigation_type="terraform",
        investigation=Investigation(
            risk_score=80.0,
        ),
        response=_response(
            risk=RiskAssessmentResponse(
                score=80,
                severity="CRITICAL",
                reasons=[],
            ),
            reasoning=ReasoningResponse(
                findings=[],
                recommendations=[],
                severity="HIGH",
            ),
        ),
    )

    assert repository.create.call_args.kwargs["severity"] == "CRITICAL"


def test_service_uses_reasoning_severity_when_risk_absent():
    repository = Mock(spec=InvestigationRepository)

    repository.create.return_value = Mock(spec=InvestigationRecord)

    service = InvestigationPersistenceService(
        repository,
    )

    service.persist(
        owner_id="owner",
        investigation_type="terraform",
        investigation=Investigation(),
        response=_response(
            reasoning=ReasoningResponse(
                findings=[],
                recommendations=[],
                severity="HIGH",
            ),
        ),
    )

    assert repository.create.call_args.kwargs["severity"] == "HIGH"


def test_service_defaults_severity_safely():
    repository = Mock(spec=InvestigationRepository)

    repository.create.return_value = Mock(spec=InvestigationRecord)

    service = InvestigationPersistenceService(
        repository,
    )

    service.persist(
        owner_id="owner",
        investigation_type="terraform",
        investigation=Investigation(),
        response=_response(),
    )

    assert repository.create.call_args.kwargs["severity"] == "LOW"


def test_service_does_not_modify_canonical_investigation():
    repository = Mock(spec=InvestigationRepository)

    repository.create.return_value = Mock(spec=InvestigationRecord)

    investigation = Investigation(
        risk_score=55.0,
        summary="Canonical state",
        analysis={
            "internal": {
                "provider_evidence": True,
            }
        },
    )

    original_analysis = investigation.analysis.copy()

    service = InvestigationPersistenceService(
        repository,
    )

    service.persist(
        owner_id="owner",
        investigation_type="terraform",
        investigation=investigation,
        response=_response(),
    )

    assert investigation.analysis == original_analysis
    assert investigation.summary == "Canonical state"
    assert investigation.risk_score == 55.0


def test_delete_delegates_to_repository():
    repository = Mock()

    repository.delete.return_value = True

    service = InvestigationPersistenceService(repository)

    result = service.delete(
        owner_id="owner-1",
        investigation_id="investigation-1",
    )

    assert result is True

    repository.delete.assert_called_once_with(
        owner_id="owner-1",
        investigation_id="investigation-1",
    )

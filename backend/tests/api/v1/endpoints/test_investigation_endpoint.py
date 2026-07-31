from unittest.mock import AsyncMock

import pytest

from fastapi import UploadFile

from app.api.v1.endpoints import investigation as endpoint
from app.domain.models import AttackPath, RiskAssessment
from app.domain.models.investigation import Investigation
from app.engines.blast_radius.models import (
    BlastRadiusAnalysis,
    BlastRadiusImpact,
)


def _investigation() -> Investigation:
    investigation = Investigation(
        risk_score=55.0,
        summary="SKYNEX endpoint investigation.",
    )

    investigation.analysis["attack_path"] = AttackPath(
        source="external-user",
        target="production-secret",
        nodes=[
            "external-user",
            "privileged-role",
            "production-secret",
        ],
        hop_count=2,
        risk="CRITICAL",
        description="Privilege-bearing attack path.",
        exists=True,
    )

    investigation.analysis["blast_radius"] = [
        "external-user",
        "privileged-role",
        "production-secret",
    ]

    investigation.analysis["blast_radius_analysis"] = BlastRadiusAnalysis(
        compromised_resource="external-user",
        reachable_resources=(
            "external-user",
            "privileged-role",
            "production-secret",
        ),
        impacts=(
            BlastRadiusImpact(
                resource_id="external-user",
                depth=0,
            ),
            BlastRadiusImpact(
                resource_id="privileged-role",
                depth=1,
                relationship_types=("allows_assume_role",),
            ),
            BlastRadiusImpact(
                resource_id="production-secret",
                depth=2,
                relationship_types=(
                    "allows_assume_role",
                    "allows_action",
                ),
            ),
        ),
    )

    investigation.analysis["risk"] = RiskAssessment(
        score=55,
        severity="MEDIUM",
        reasons=[
            "CRITICAL attack path exists.",
        ],
    )

    return investigation


@pytest.mark.anyio
async def test_terraform_endpoint_uses_public_response_mapping(
    monkeypatch,
):
    mocked = AsyncMock(return_value=_investigation())

    monkeypatch.setattr(
        endpoint.orchestrator,
        "investigate_terraform",
        mocked,
    )

    upload = UploadFile(
        filename="main.tf",
        file=None,
    )

    response = await endpoint.investigate_terraform(
        terraform_file=upload,
        source="external-user",
        target="production-secret",
    )

    assert response.attack_path == [
        "external-user",
        "privileged-role",
        "production-secret",
    ]

    assert response.attack_path_analysis is not None
    assert response.attack_path_analysis.risk == "CRITICAL"

    assert response.blast_radius_analysis is not None
    assert response.blast_radius_analysis.affected_resource_count == 2
    assert response.blast_radius_analysis.maximum_depth == 2

    assert response.risk is not None
    assert response.risk.score == 55
    assert response.risk.severity == "MEDIUM"

    assert response.reasoning is not None
    assert response.reasoning.findings
    assert response.reasoning.recommendations

    mocked.assert_awaited_once_with(
        terraform_file=upload,
        source="external-user",
        target="production-secret",
    )


@pytest.mark.anyio
async def test_terraform_endpoint_response_is_serializable(
    monkeypatch,
):
    monkeypatch.setattr(
        endpoint.orchestrator,
        "investigate_terraform",
        AsyncMock(return_value=_investigation()),
    )

    upload = UploadFile(
        filename="main.tf",
        file=None,
    )

    response = await endpoint.investigate_terraform(
        terraform_file=upload,
        source="external-user",
        target="production-secret",
    )

    payload = response.model_dump(mode="json")

    assert payload["risk_score"] == 55.0
    assert payload["attack_path_analysis"]["risk"] == "CRITICAL"
    assert payload["risk"]["severity"] == "MEDIUM"
    assert payload["reasoning"]["severity"] == "MEDIUM"

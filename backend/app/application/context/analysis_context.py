from dataclasses import dataclass, field

from app.domain.models import AttackPath, RiskAssessment
from app.domain.models.relationship import Relationship
from app.domain.models.resource import Resource


@dataclass(slots=True)
class AnalysisContext:
    """
    Consolidated view of an investigation.

    This object provides downstream components (AI,
    reporting, remediation, dashboards, etc.) with a
    stable interface instead of exposing the raw
    investigation.analysis dictionary.
    """

    resources: list[Resource] = field(default_factory=list)

    relationships: list[Relationship] = field(default_factory=list)

    attack_path: AttackPath | None = None

    blast_radius: list[str] = field(default_factory=list)

    risk: RiskAssessment | None = None

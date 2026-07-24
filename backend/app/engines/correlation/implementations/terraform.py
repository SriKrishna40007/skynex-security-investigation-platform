from __future__ import annotations

from app.domain.models.investigation import Investigation
from app.engines.correlation.base import CorrelationEngine
from app.engines.correlation.builders.terraform_relationship_builder import (
    TerraformRelationshipBuilder,
)


class TerraformCorrelationEngine(CorrelationEngine):
    """
    Correlates canonical Terraform resources by discovering
    relationships between them.
    """

    def __init__(self) -> None:
        self._relationship_builder = TerraformRelationshipBuilder()

    def correlate(
        self,
        investigation: Investigation,
    ) -> Investigation:
        investigation.relationships = (
            self._relationship_builder.build(
                investigation.resources,
            )
        )

        return investigation

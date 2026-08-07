import json

from app.models import InvestigationRecord
from app.schemas.export import InvestigationExportResponse


class InvestigationExportService:
    """
    Builds export payloads for investigations.
    """

    def export(
        self,
        investigation: InvestigationRecord,
        export_format: str,
    ) -> InvestigationExportResponse:

        export_format = export_format.lower()

        if export_format == "json":
            content = json.dumps(
                investigation.result,
                indent=2,
                default=str,
            )

            return InvestigationExportResponse(
                filename=f"{investigation.id}.json",
                content_type="application/json",
                content=content,
            )

        markdown = f"""# Investigation

**ID:** {investigation.id}

**Type:** {investigation.investigation_type}

**Status:** {investigation.status}

**Severity:** {investigation.severity}

**Risk Score:** {investigation.risk_score}

## Summary

{investigation.summary}
"""

        return InvestigationExportResponse(
            filename=f"{investigation.id}.md",
            content_type="text/markdown",
            content=markdown,
        )

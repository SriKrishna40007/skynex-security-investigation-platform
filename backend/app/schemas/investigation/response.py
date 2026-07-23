"""
Public API response for investigation endpoints.
"""

from app.schemas.investigation.report import InvestigationReport


class InvestigationResponse(InvestigationReport):
    """
    Public response model.
    """

    pass

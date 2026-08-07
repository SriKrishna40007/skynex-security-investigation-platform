from pydantic import BaseModel


class InvestigationExportResponse(BaseModel):
    """
    Export payload returned for investigation downloads.
    """

    filename: str

    content_type: str

    content: str

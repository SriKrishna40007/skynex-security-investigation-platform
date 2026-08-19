from typing import Any

from pydantic import BaseModel, Field


class ResourceResponse(BaseModel):
    """
    Public representation of a canonical SKYNEX cloud resource.
    """

    id: str
    name: str
    type: str
    provider: str
    tags: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

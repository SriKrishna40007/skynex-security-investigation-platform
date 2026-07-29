from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    """Request used to rotate an authenticated session."""

    refresh_token: str = Field(
        ...,
        min_length=32,
        max_length=512,
    )

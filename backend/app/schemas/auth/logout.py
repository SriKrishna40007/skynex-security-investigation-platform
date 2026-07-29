from pydantic import BaseModel, Field


class LogoutRequest(BaseModel):
    """Request used to revoke an authenticated session."""

    refresh_token: str = Field(
        ...,
        min_length=32,
        max_length=512,
    )

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Authentication tokens issued for a persistent user session."""

    access_token: str
    refresh_token: str
    session_id: str
    token_type: str = "bearer"

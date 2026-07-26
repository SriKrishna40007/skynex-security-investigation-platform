from pydantic import BaseModel


class TokenResponse(BaseModel):
    """JWT authentication response."""

    access_token: str
    token_type: str = "bearer"

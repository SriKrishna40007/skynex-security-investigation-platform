from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Request payload for user login."""

    email: EmailStr
    password: str

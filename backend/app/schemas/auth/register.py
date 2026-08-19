from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request payload for user registration."""

    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class RegisterResponse(BaseModel):
    """Response returned after successful registration."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: EmailStr
    is_active: bool
    verification_required: bool = True
    message: str = "Account created. Please verify your email before signing in."


class VerifyEmailRequest(BaseModel):
    """Request payload for email verification."""

    token: str = Field(..., min_length=20, max_length=512)


class VerifyEmailResponse(BaseModel):
    """Response returned after successful email verification."""

    message: str
    email_verified: bool = True

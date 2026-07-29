from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """
    API request for registering a new user.
    """

    full_name: str = Field(
        min_length=2,
        max_length=255,
        description="User full name",
    )

    email: EmailStr = Field(
        description="User email address",
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password",
    )


class LoginRequest(BaseModel):
    """
    API request for authenticating an existing user.
    """

    email: EmailStr = Field(
        description="User email address",
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password",
    )


class TokenResponse(BaseModel):
    """
    Authentication response returned after a successful login.
    """

    access_token: str = Field(
        description="JWT access token",
    )

    token_type: str = Field(
        default="bearer",
        description="Authentication scheme",
    )

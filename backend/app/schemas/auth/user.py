from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    """Authenticated user response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: EmailStr
    is_active: bool

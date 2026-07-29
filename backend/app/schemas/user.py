from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    """
    Public representation of a user.
    """

    id: str

    full_name: str

    email: EmailStr

    role: str

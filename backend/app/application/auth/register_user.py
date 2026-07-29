from app.core.security import hash_password
from app.exceptions import UserAlreadyExistsError
from app.repositories import UserRepository
from app.schemas.auth import RegisterRequest, RegisterResponse


class RegisterUserUseCase:
    """Business use case for registering a new user."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, request: RegisterRequest) -> RegisterResponse:
        existing_user = self.repository.get_by_email(request.email)

        if existing_user:
            raise UserAlreadyExistsError("A user with this email already exists.")

        user = self.repository.create(
            full_name=request.full_name,
            email=request.email,
            password_hash=hash_password(request.password),
        )

        return RegisterResponse.model_validate(user)

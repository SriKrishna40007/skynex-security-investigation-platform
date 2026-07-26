from app.core.security import create_access_token, verify_password
from app.exceptions import InvalidCredentialsError
from app.repositories import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse


class LoginUserUseCase:
    """Business use case for authenticating a user."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, request: LoginRequest) -> TokenResponse:
        user = self.repository.get_by_email(request.email)

        if user is None:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError("Invalid email or password.")

        access_token = create_access_token(user.id)

        return TokenResponse(
            access_token=access_token,
        )

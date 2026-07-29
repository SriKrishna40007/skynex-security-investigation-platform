from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    refresh_token_expiry,
    utc_now,
    verify_password,
)
from app.exceptions import InvalidCredentialsError
from app.repositories import SessionRepository, UserRepository
from app.schemas.auth import LoginRequest, TokenResponse


class LoginUserUseCase:
    """Authenticate a user and establish a persistent server-side session."""

    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository

    def execute(
        self,
        request: LoginRequest,
        *,
        device_name: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> TokenResponse:
        user = self.user_repository.get_by_email(request.email)

        if user is None:
            raise InvalidCredentialsError("Invalid email or password.")

        if not user.is_active:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError("Invalid email or password.")

        access_token = create_access_token(user.id)
        refresh_token = generate_refresh_token()

        now = utc_now()

        session = self.session_repository.create(
            user_id=user.id,
            refresh_token_hash=hash_refresh_token(refresh_token),
            expires_at=refresh_token_expiry(),
            last_used_at=now,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            session_id=session.id,
        )

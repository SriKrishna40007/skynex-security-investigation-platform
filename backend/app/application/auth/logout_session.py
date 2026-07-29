from app.core.security import hash_refresh_token
from app.exceptions import InvalidCredentialsError
from app.repositories import SessionRepository


class LogoutSessionUseCase:
    """Revoke the server-side session associated with a refresh token."""

    def __init__(
        self,
        session_repository: SessionRepository,
    ):
        self.session_repository = session_repository

    def execute(self, refresh_token: str) -> None:
        session = self.session_repository.get_by_refresh_token_hash(
            hash_refresh_token(refresh_token)
        )

        if session is None:
            raise InvalidCredentialsError("Invalid refresh token.")

        if session.is_revoked:
            return

        self.session_repository.revoke(session)

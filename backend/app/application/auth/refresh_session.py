from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    refresh_token_expiry,
    utc_now,
)
from app.exceptions import InvalidCredentialsError
from app.repositories import SessionRepository, UserRepository
from app.schemas.auth import TokenResponse


class RefreshSessionUseCase:
    """Rotate a valid refresh token and issue a new token pair."""

    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository

    def execute(self, refresh_token: str) -> TokenResponse:
        now = utc_now()

        session = self.session_repository.get_by_refresh_token_hash(
            hash_refresh_token(refresh_token)
        )

        if session is None:
            raise InvalidCredentialsError("Invalid refresh token.")

        if session.is_revoked:
            raise InvalidCredentialsError("Session has been revoked.")

        expires_at = session.expires_at

        # PostgreSQL TIMESTAMP may be returned as timezone-naive because the
        # current schema uses DateTime without timezone=True.
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=now.tzinfo)

        if expires_at <= now:
            self.session_repository.revoke(session)
            raise InvalidCredentialsError("Refresh token has expired.")

        user = self.user_repository.get_by_id(session.user_id)

        if user is None or not user.is_active:
            self.session_repository.revoke(session)
            raise InvalidCredentialsError("User session is no longer valid.")

        new_refresh_token = generate_refresh_token()

        self.session_repository.rotate_refresh_token(
            session,
            refresh_token_hash=hash_refresh_token(new_refresh_token),
            expires_at=refresh_token_expiry(),
            last_used_at=now,
        )

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=new_refresh_token,
            session_id=session.id,
        )

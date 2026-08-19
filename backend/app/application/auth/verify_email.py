from datetime import datetime, timezone

from app.application.auth.email_verification import hash_verification_token
from app.exceptions import InvalidEmailVerificationTokenError
from app.repositories import EmailVerificationTokenRepository, UserRepository
from app.schemas.auth import VerifyEmailResponse


class VerifyEmailUseCase:
    """Verify ownership of a user's email address."""

    def __init__(
        self,
        user_repository: UserRepository,
        verification_repository: EmailVerificationTokenRepository,
    ):
        self.user_repository = user_repository
        self.verification_repository = verification_repository

    def execute(self, token: str) -> VerifyEmailResponse:
        token_hash = hash_verification_token(token)

        verification_token = self.verification_repository.get_by_hash(token_hash)

        if verification_token is None:
            raise InvalidEmailVerificationTokenError(
                "Invalid or expired verification link."
            )

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        if verification_token.used_at is not None:
            raise InvalidEmailVerificationTokenError(
                "Invalid or expired verification link."
            )

        if verification_token.expires_at <= now:
            raise InvalidEmailVerificationTokenError(
                "Invalid or expired verification link."
            )

        user = self.user_repository.get_by_id(verification_token.user_id)

        if user is None or not user.is_active:
            raise InvalidEmailVerificationTokenError(
                "Invalid or expired verification link."
            )

        user.email_verified_at = now
        verification_token.used_at = now

        self.user_repository.commit()

        return VerifyEmailResponse(
            message="Email verified successfully. You can now sign in.",
        )

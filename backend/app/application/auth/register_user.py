from datetime import datetime, timedelta, timezone

from app.application.auth.development_email_service import DevelopmentEmailService
from app.application.auth.email_service import EmailService
from app.application.auth.email_verification import (
    generate_verification_token,
    hash_verification_token,
)
from app.core.security import hash_password
from app.exceptions import UserAlreadyExistsError
from app.repositories import (
    EmailVerificationTokenRepository,
    UserRepository,
)
from app.schemas.auth import RegisterRequest, RegisterResponse


VERIFICATION_TOKEN_TTL = timedelta(minutes=30)


class RegisterUserUseCase:
    """Register a user and establish an email-verification challenge."""

    def __init__(
        self,
        user_repository: UserRepository,
        verification_repository: EmailVerificationTokenRepository,
        email_service: EmailService | None = None,
    ):
        self.user_repository = user_repository
        self.verification_repository = verification_repository
        self.email_service = email_service or DevelopmentEmailService()

    def execute(self, request: RegisterRequest) -> RegisterResponse:
        existing_user = self.user_repository.get_by_email(request.email)

        if existing_user:
            raise UserAlreadyExistsError("A user with this email already exists.")

        user = self.user_repository.create(
            full_name=request.full_name,
            email=request.email,
            password_hash=hash_password(request.password),
        )

        raw_token = generate_verification_token()
        token_hash = hash_verification_token(raw_token)

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        self.verification_repository.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=now + VERIFICATION_TOKEN_TTL,
            created_at=now,
        )

        # Both the user and verification challenge are committed together.
        self.user_repository.commit()
        self.user_repository.refresh(user)

        verification_url = f"http://localhost:5173/verify-email?token={raw_token}"

        self.email_service.send_verification_email(
            recipient=user.email,
            verification_url=verification_url,
        )

        return RegisterResponse.model_validate(user)

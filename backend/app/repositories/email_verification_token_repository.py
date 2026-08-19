from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.email_verification_token import EmailVerificationToken


class EmailVerificationTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        user_id: str,
        token_hash: str,
        expires_at: datetime,
        created_at: datetime,
    ) -> EmailVerificationToken:
        token = EmailVerificationToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=created_at,
        )

        self.db.add(token)
        self.db.flush()

        return token

    def get_by_hash(
        self,
        token_hash: str,
    ) -> EmailVerificationToken | None:
        statement = select(EmailVerificationToken).where(
            EmailVerificationToken.token_hash == token_hash
        )

        return self.db.scalar(statement)

    def revoke_unused_for_user(
        self,
        *,
        user_id: str,
        revoked_at: datetime,
    ) -> None:
        statement = select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == user_id,
            EmailVerificationToken.used_at.is_(None),
        )

        tokens = self.db.scalars(statement).all()

        for token in tokens:
            token.used_at = revoked_at

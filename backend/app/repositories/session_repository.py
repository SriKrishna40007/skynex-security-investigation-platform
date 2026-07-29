from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session as DatabaseSession

from app.models import Session


class SessionRepository:
    """Persistence operations for authenticated user sessions."""

    def __init__(self, db: DatabaseSession):
        self.db = db

    def create(
        self,
        *,
        user_id: str,
        refresh_token_hash: str,
        expires_at: datetime,
        last_used_at: datetime,
        device_name: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> Session:
        session = Session(
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            last_used_at=last_used_at,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_by_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> Session | None:
        statement = select(Session).where(
            Session.refresh_token_hash == refresh_token_hash
        )

        return self.db.scalar(statement)

    def list_active_for_user(
        self,
        user_id: str,
        now: datetime,
    ) -> list[Session]:
        statement = select(Session).where(
            Session.user_id == user_id,
            Session.is_revoked.is_(False),
            Session.expires_at > now,
        )

        return list(self.db.scalars(statement).all())

    def rotate_refresh_token(
        self,
        session: Session,
        *,
        refresh_token_hash: str,
        expires_at: datetime,
        last_used_at: datetime,
    ) -> Session:
        session.refresh_token_hash = refresh_token_hash
        session.expires_at = expires_at
        session.last_used_at = last_used_at

        self.db.commit()
        self.db.refresh(session)

        return session

    def revoke(self, session: Session) -> None:
        session.is_revoked = True
        self.db.commit()

    def revoke_all_for_user(self, user_id: str) -> None:
        statement = select(Session).where(
            Session.user_id == user_id,
            Session.is_revoked.is_(False),
        )

        sessions = self.db.scalars(statement).all()

        for session in sessions:
            session.is_revoked = True

        self.db.commit()

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Role, User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_default_role(self) -> Role:
        statement = select(Role).where(Role.name == "viewer")
        role = self.db.scalar(statement)

        if role is None:
            raise RuntimeError(
                "Default role 'viewer' does not exist. Seed roles first."
            )

        return role

    def create(
        self,
        *,
        full_name: str,
        email: str,
        password_hash: str,
    ) -> User:
        role = self.get_default_role()

        user = User(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

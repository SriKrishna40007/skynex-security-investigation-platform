from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Role


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Role | None:
        statement = select(Role).where(Role.name == name)
        return self.db.scalar(statement)

    def create(
        self,
        *,
        name: str,
        description: str,
    ) -> Role:
        role = Role(
            name=name,
            description=description,
        )

        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        return role

    def list(self) -> list[Role]:
        statement = select(Role)
        return list(self.db.scalars(statement).all())

from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.api.v1.dependencies.auth import get_current_user
from app.models.user import User


def require_role(*roles: str) -> Callable:
    if not roles:
        raise ValueError("At least one role must be provided.")

    allowed_roles = frozenset(roles)

    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role.",
            )

        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )

        return current_user

    return dependency

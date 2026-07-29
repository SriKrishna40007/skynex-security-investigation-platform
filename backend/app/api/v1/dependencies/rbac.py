from fastapi import Depends, HTTPException, status

from app.api.v1.dependencies.auth import get_current_user


def require_role(*roles: str):
    def dependency(current_user=Depends(get_current_user)):
        if current_user.role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role.",
            )

        if current_user.role.name not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )

        return current_user

    return dependency

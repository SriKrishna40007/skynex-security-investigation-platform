from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(subject: str) -> str:
    """Create a signed JWT access token."""

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> str:
    """
    Validate a JWT and return the subject (user id).
    """

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        subject = payload.get("sub")

        if subject is None:
            raise ValueError("Token does not contain a subject.")

        return subject

    except JWTError as exc:
        raise ValueError("Invalid or expired token.") from exc

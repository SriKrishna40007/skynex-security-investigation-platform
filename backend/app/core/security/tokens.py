import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from app.core.config import settings


def generate_refresh_token() -> str:
    """Generate a cryptographically secure opaque refresh token."""
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    """Create the deterministic SHA-256 digest stored for a refresh token."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def refresh_token_expiry() -> datetime:
    """Return the UTC expiry time for a refresh-token session."""
    return datetime.now(UTC) + timedelta(
        days=settings.refresh_token_expire_days,
    )


def utc_now() -> datetime:
    """Return the current timezone-aware UTC time."""
    return datetime.now(UTC)

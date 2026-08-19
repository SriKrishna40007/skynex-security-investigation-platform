import hashlib
import secrets


TOKEN_BYTES = 32


def generate_verification_token() -> str:
    """Generate a cryptographically secure verification token."""
    return secrets.token_urlsafe(TOKEN_BYTES)


def hash_verification_token(token: str) -> str:
    """Hash a verification token before persistence."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

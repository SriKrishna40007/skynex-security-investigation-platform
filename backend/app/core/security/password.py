from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain text password using Argon2."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain text password against its hash."""
    return password_hasher.verify(password, password_hash)

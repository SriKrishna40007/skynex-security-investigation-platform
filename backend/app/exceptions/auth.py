class AuthenticationError(Exception):
    """Base exception for authentication errors."""


class UserAlreadyExistsError(AuthenticationError):
    """Raised when a user tries to register with an existing email."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are invalid."""


class InvalidEmailVerificationTokenError(AuthenticationError):
    """Raised when an email verification token is invalid, expired, or used."""

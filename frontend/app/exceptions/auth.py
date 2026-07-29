class AuthenticationError(Exception):
    """Base exception for authentication errors."""


class UserAlreadyExistsError(AuthenticationError):
    """Raised when a user tries to register with an existing email."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are invalid."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationEmail:
    recipient: str
    verification_url: str


class EmailService:
    """Boundary for transactional email delivery."""

    def send_verification_email(
        self,
        *,
        recipient: str,
        verification_url: str,
    ) -> None:
        raise NotImplementedError

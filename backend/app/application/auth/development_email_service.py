import logging

from app.application.auth.email_service import EmailService


logger = logging.getLogger(__name__)


class DevelopmentEmailService(EmailService):
    """
    Development email adapter.

    The verification URL is logged locally so the complete
    registration -> verification flow can be exercised without
    requiring an external email provider.
    """

    def send_verification_email(
        self,
        *,
        recipient: str,
        verification_url: str,
    ) -> None:
        logger.info(
            "EMAIL_VERIFICATION recipient=%s verification_url=%s",
            recipient,
            verification_url,
        )

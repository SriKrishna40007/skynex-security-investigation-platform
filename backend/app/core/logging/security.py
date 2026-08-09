import logging
from typing import Any

security_logger = logging.getLogger("skynex.security")


def security_event(
    event: str,
    *,
    success: bool,
    user_id: str | None = None,
    ip_address: str | None = None,
    **details: Any,
) -> None:
    payload = {
        "event": event,
        "success": success,
        "user_id": user_id,
        "ip_address": ip_address,
        **details,
    }

    security_logger.info("security_event=%s", payload)

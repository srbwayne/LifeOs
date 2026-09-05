from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from app.read.application.ports.progression_gateway import (
    ProgressionDeliveryResult,
    ReadingProgressionFact,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LogosProgressionSettings:
    base_url: str | None
    enabled: bool
    timeout_seconds: float
    bearer_token: str | None

    @classmethod
    def from_environment(cls) -> LogosProgressionSettings:
        enabled = os.getenv("LOGOS_ENABLED", "false").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        raw_timeout = os.getenv("LOGOS_TIMEOUT", "5").strip()
        try:
            timeout = float(raw_timeout)
        except ValueError as exc:
            raise ValueError("LOGOS_TIMEOUT must be a positive number") from exc
        if timeout <= 0:
            raise ValueError("LOGOS_TIMEOUT must be a positive number")
        return cls(
            base_url=os.getenv("LOGOS_BASE_URL"),
            enabled=enabled,
            timeout_seconds=timeout,
            bearer_token=os.getenv("LOGOS_BEARER_TOKEN"),
        )


class LogosProgressionGateway:
    def __init__(self, settings: LogosProgressionSettings) -> None:
        self._settings = settings

    def evaluate_reading_session(self, fact: ReadingProgressionFact) -> ProgressionDeliveryResult:
        if not self._settings.enabled:
            logger.info("Logos progression integration disabled")
            return ProgressionDeliveryResult(success=False, error="disabled")
        if not self._settings.base_url:
            logger.error("Logos progression integration enabled without LOGOS_BASE_URL")
            return ProgressionDeliveryResult(success=False, error="missing_base_url")
        if not self._settings.bearer_token:
            logger.error("Logos progression integration enabled without LOGOS_BEARER_TOKEN")
            return ProgressionDeliveryResult(success=False, error="missing_bearer_token")

        url = (
            f"{self._settings.base_url.rstrip('/')}/api/internal/v3/progression/external/"
            f"lifeos/{quote(str(fact.user_id), safe='')}/evaluate"
        )
        payload = {
            "execution": {
                "source": "lifeos",
                "idempotencyKey": fact.source_event_id,
            },
            "configuration": {"key": "reading"},
            "details": [{"factorKey": "pages_read", "value": fact.pages_read}],
        }
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._settings.bearer_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self._settings.timeout_seconds) as response:
                response.read()
                status_code = response.status
            logger.info(
                "LifeOS reading progression delivered",
                extra={
                    "reading_session_id": fact.source_event_id,
                    "user_id": str(fact.user_id),
                    "status_code": status_code,
                },
            )
            return ProgressionDeliveryResult(
                success=200 <= status_code < 300, status_code=status_code
            )
        except HTTPError as error:
            logger.error(
                "Logos rejected LifeOS reading progression",
                extra={
                    "reading_session_id": fact.source_event_id,
                    "user_id": str(fact.user_id),
                    "status_code": error.code,
                },
            )
            return ProgressionDeliveryResult(
                success=False, status_code=error.code, error="http_error"
            )
        except (TimeoutError, URLError, OSError) as error:
            logger.error(
                "Logos reading progression delivery failed",
                extra={
                    "reading_session_id": fact.source_event_id,
                    "user_id": str(fact.user_id),
                    "error": type(error).__name__,
                },
            )
            return ProgressionDeliveryResult(success=False, error=type(error).__name__)

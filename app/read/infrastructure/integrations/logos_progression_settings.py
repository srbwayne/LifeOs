from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from urllib.parse import urlparse


class LogosProgressionConfigurationError(ValueError):
    """Raised when the explicitly enabled Logos integration is invalid."""


@dataclass(frozen=True)
class LogosProgressionSettings:
    enabled: bool = False
    base_url: str | None = None
    bearer_token: str | None = field(default=None, repr=False)
    reading_configuration_key: str | None = None
    reading_configuration_revision: int | None = None
    timeout_seconds: float | None = None

    @classmethod
    def from_environment(cls) -> LogosProgressionSettings:
        enabled = _parse_bool(_read("LIFEOS_LOGOS_PROGRESSION_ENABLED", "false"))
        if not enabled:
            return cls()

        base_url = _required("LIFEOS_LOGOS_BASE_URL")
        _validate_base_url(base_url)
        bearer_token = _required("LIFEOS_LOGOS_BEARER_TOKEN")
        configuration_key = _required("LIFEOS_LOGOS_READING_CONFIGURATION_KEY")
        timeout_seconds = _parse_timeout(_required("LIFEOS_LOGOS_TIMEOUT_SECONDS"))
        revision = _parse_revision(os.getenv("LIFEOS_LOGOS_READING_CONFIGURATION_REVISION"))
        return cls(
            enabled=True,
            base_url=base_url,
            bearer_token=bearer_token,
            reading_configuration_key=configuration_key,
            reading_configuration_revision=revision,
            timeout_seconds=timeout_seconds,
        )


def _read(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def _required(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise LogosProgressionConfigurationError(
            f"{name} is required when Logos progression is enabled."
        )
    return value.strip()


def _parse_bool(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise LogosProgressionConfigurationError(
        "LIFEOS_LOGOS_PROGRESSION_ENABLED must be true or false."
    )


def _validate_base_url(value: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise LogosProgressionConfigurationError(
            "LIFEOS_LOGOS_BASE_URL must be a valid HTTP or HTTPS URL."
        )


def _parse_revision(value: str | None) -> int | None:
    if value is None or not value.strip():
        return None
    try:
        revision = int(value.strip())
    except ValueError as error:
        raise LogosProgressionConfigurationError(
            "LIFEOS_LOGOS_READING_CONFIGURATION_REVISION must be a positive integer."
        ) from error
    if revision <= 0:
        raise LogosProgressionConfigurationError(
            "LIFEOS_LOGOS_READING_CONFIGURATION_REVISION must be a positive integer."
        )
    return revision


def _parse_timeout(value: str) -> float:
    try:
        timeout = float(value.strip())
    except ValueError as error:
        raise LogosProgressionConfigurationError(
            "LIFEOS_LOGOS_TIMEOUT_SECONDS must be finite and greater than zero."
        ) from error
    if not math.isfinite(timeout) or timeout <= 0:
        raise LogosProgressionConfigurationError(
            "LIFEOS_LOGOS_TIMEOUT_SECONDS must be finite and greater than zero."
        )
    return timeout

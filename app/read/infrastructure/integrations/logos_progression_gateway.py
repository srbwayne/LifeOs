from __future__ import annotations

from typing import Any

import httpx

from app.read.application.ports.progression_gateway import (
    ProgressionGateway,
    ProgressionGatewayError,
    ReadingProgressionOccurrence,
)
from app.read.infrastructure.integrations.logos_progression_settings import (
    LogosProgressionSettings,
)

_EXECUTIONS_PATH = "/api/internal/v1/progression/executions"


class LogosProgressionGatewayError(ProgressionGatewayError):
    def __init__(self, classification: str, message: str) -> None:
        self.classification = classification
        super().__init__(message)


class LogosProgressionGateway(ProgressionGateway):
    def __init__(
        self,
        settings: LogosProgressionSettings,
        client: httpx.Client | None = None,
    ) -> None:
        if not settings.enabled or settings.base_url is None or settings.bearer_token is None:
            raise ValueError("LogosProgressionGateway requires enabled settings.")
        if (
            settings.reading_configuration_key is None
            or settings.reading_configuration_revision is None
            or settings.timeout_seconds is None
        ):
            raise ValueError("LogosProgressionGateway requires complete settings.")
        if settings.reading_configuration_revision <= 0:
            raise ValueError("LogosProgressionGateway requires a positive configuration revision.")
        self._settings = settings
        self._client = client
        self._url = f"{settings.base_url.rstrip('/')}{_EXECUTIONS_PATH}"

    def record(self, occurrence: ReadingProgressionOccurrence) -> None:
        payload = {
            "subject": {
                "namespace": "lifeos",
                "externalId": occurrence.owner_id.to_persistence(),
            },
            "execution": {
                "source": "lifeos",
                "idempotencyKey": (
                    f"reading-session:{occurrence.reading_session_id.to_persistence()}"
                ),
            },
            "configuration": {
                "key": self._settings.reading_configuration_key,
                "revision": self._settings.reading_configuration_revision,
            },
            "details": [
                {"factorKey": "pages_read", "value": occurrence.pages_read},
            ],
        }
        if self._client is not None:
            self._post(self._client, payload)
            return

        with httpx.Client(timeout=self._settings.timeout_seconds) as client:
            self._post(client, payload)

    def _post(self, client: httpx.Client, payload: dict[str, Any]) -> None:
        try:
            response = client.post(
                self._url,
                json=payload,
                headers={"Authorization": f"Bearer {self._settings.bearer_token}"},
            )
        except httpx.TimeoutException as error:
            raise LogosProgressionGatewayError(
                "logos_timeout", "Logos request timed out."
            ) from error
        except httpx.RequestError as error:
            raise LogosProgressionGatewayError(
                "logos_network_failure", "Logos request failed at the network boundary."
            ) from error

        if response.status_code == 200:
            return
        raise _response_error(response)


def _response_error(response: httpx.Response) -> LogosProgressionGatewayError:
    status = response.status_code
    if status == 400:
        return LogosProgressionGatewayError("http_status_400", "Logos rejected the request.")
    if status == 401:
        return LogosProgressionGatewayError(
            "logos_http_401_operator_action", "Logos authentication requires operator action."
        )
    if status == 403:
        return LogosProgressionGatewayError(
            "logos_http_403_operator_action", "Logos authorization requires operator action."
        )
    if status == 404:
        return LogosProgressionGatewayError(
            "logos_http_404_prerequisite", "A Logos progression prerequisite is unavailable."
        )
    if status == 409:
        if _response_code(response) == "PROGRESSION_CONFIGURATION_NOT_ACTIVE":
            return LogosProgressionGatewayError(
                "logos_configuration_inactive",
                "Logos progression configuration requires operator action.",
            )
        return LogosProgressionGatewayError(
            "http_status_409", "Logos reported an execution conflict."
        )
    if status == 429:
        return LogosProgressionGatewayError(
            "logos_http_429_retryable", "Logos rate limiting requires a later attempt."
        )
    if 500 <= status < 600:
        return LogosProgressionGatewayError(
            "logos_http_5xx_retryable", "Logos reported a server failure."
        )
    return LogosProgressionGatewayError(
        "logos_http_status_retryable", "Logos returned an unsupported failure status."
    )


def _response_code(response: httpx.Response) -> str | None:
    try:
        body: Any = response.json()
    except ValueError:
        return None
    return (
        body.get("code") if isinstance(body, dict) and isinstance(body.get("code"), str) else None
    )

from __future__ import annotations

import json

import httpx
import pytest

from app.read.application.ports.progression_gateway import ReadingProgressionOccurrence
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.infrastructure.integrations.logos_progression_gateway import (
    LogosProgressionGateway,
    LogosProgressionGatewayError,
)
from app.read.infrastructure.integrations.logos_progression_settings import (
    LogosProgressionSettings,
)
from app.shared.domain.identifiers.user_id import UserId


def _settings(revision: int | None = None) -> LogosProgressionSettings:
    return LogosProgressionSettings(
        enabled=True,
        base_url="https://logos.example/",
        bearer_token="fake-token",
        reading_configuration_key="reading-v1",
        reading_configuration_revision=revision,
        timeout_seconds=2.0,
    )


def _occurrence() -> ReadingProgressionOccurrence:
    return ReadingProgressionOccurrence(UserId.new(), ReadingSessionId.new(), 30)


def test_success_maps_supported_logos_request_exactly() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"status": "accepted"}, request=request)

    gateway = LogosProgressionGateway(
        _settings(3), httpx.Client(transport=httpx.MockTransport(handler))
    )
    occurrence = _occurrence()
    gateway.record(occurrence)

    request = requests[0]
    assert request.method == "POST"
    assert str(request.url) == "https://logos.example/api/internal/v1/progression/executions"
    assert request.headers["Authorization"] == "Bearer fake-token"
    assert request.read().decode() == request.content.decode()
    body = json.loads(request.content)
    assert body == {
        "subject": {"namespace": "lifeos", "externalId": occurrence.owner_id.to_persistence()},
        "execution": {
            "source": "lifeos",
            "idempotencyKey": f"reading-session:{occurrence.reading_session_id.to_persistence()}",
        },
        "configuration": {"key": "reading-v1", "revision": 3},
        "details": [{"factorKey": "pages_read", "value": 30}],
    }
    assert "notes" not in body
    assert "book" not in str(body).lower()


@pytest.mark.parametrize(
    ("status", "classification"),
    [
        (400, "http_status_400"),
        (401, "logos_http_401_operator_action"),
        (403, "logos_http_403_operator_action"),
        (404, "logos_http_404_prerequisite"),
        (429, "logos_http_429_retryable"),
        (500, "logos_http_5xx_retryable"),
        (503, "logos_http_5xx_retryable"),
    ],
)
def test_http_failure_classification(status, classification) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text="sensitive remote detail", request=request)

    gateway = LogosProgressionGateway(
        _settings(), httpx.Client(transport=httpx.MockTransport(handler))
    )
    with pytest.raises(LogosProgressionGatewayError) as error:
        gateway.record(_occurrence())
    assert error.value.classification == classification
    assert "sensitive" not in str(error.value)


def test_configuration_inactive_409_is_recoverable() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            409,
            json={"code": "PROGRESSION_CONFIGURATION_NOT_ACTIVE"},
            request=request,
        )

    gateway = LogosProgressionGateway(
        _settings(), httpx.Client(transport=httpx.MockTransport(handler))
    )
    with pytest.raises(LogosProgressionGatewayError) as error:
        gateway.record(_occurrence())
    assert error.value.classification == "logos_configuration_inactive"


@pytest.mark.parametrize("body", [{"code": "OTHER"}, {"unexpected": True}, "malformed"])
def test_unknown_or_malformed_409_is_terminal(body) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(409, json=body, request=request)

    gateway = LogosProgressionGateway(
        _settings(), httpx.Client(transport=httpx.MockTransport(handler))
    )
    with pytest.raises(LogosProgressionGatewayError) as error:
        gateway.record(_occurrence())
    assert error.value.classification == "http_status_409"


def test_network_failure_is_nonterminal() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("offline", request=request)

    gateway = LogosProgressionGateway(
        _settings(), httpx.Client(transport=httpx.MockTransport(handler))
    )
    with pytest.raises(LogosProgressionGatewayError) as error:
        gateway.record(_occurrence())
    assert error.value.classification == "logos_network_failure"


def test_timeout_is_nonterminal() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=request)

    gateway = LogosProgressionGateway(
        _settings(), httpx.Client(transport=httpx.MockTransport(handler))
    )
    with pytest.raises(LogosProgressionGatewayError) as error:
        gateway.record(_occurrence())
    assert error.value.classification == "logos_timeout"

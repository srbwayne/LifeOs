import json
from urllib.error import HTTPError

from app.read.application.ports.progression_gateway import ReadingProgressionFact
from app.read.infrastructure.integrations.logos_progression_gateway import (
    LogosProgressionGateway,
    LogosProgressionSettings,
)
from app.shared.domain.identifiers.user_id import UserId


class FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return b'{"result": {}, "profile": {}}'


def test_gateway_maps_reading_session_to_exact_logos_v3_request(monkeypatch) -> None:
    captured = {}
    user_id = UserId.new()

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(
        "app.read.infrastructure.integrations.logos_progression_gateway.urlopen",
        fake_urlopen,
    )
    gateway = LogosProgressionGateway(
        LogosProgressionSettings("http://logos.test", True, 3.5, "token-from-env")
    )

    result = gateway.evaluate_reading_session(
        ReadingProgressionFact("reading-session-1", user_id, 30)
    )

    assert result.success is True
    assert captured["timeout"] == 3.5
    request = captured["request"]
    assert request.full_url == (
        "http://logos.test/api/internal/v3/progression/external/lifeos/"
        + str(user_id)
        + "/evaluate"
    )
    assert request.get_method() == "POST"
    assert request.get_header("Authorization") == "Bearer token-from-env"
    assert json.loads(request.data.decode()) == {
        "execution": {"source": "lifeos", "idempotencyKey": "reading-session-1"},
        "configuration": {"key": "reading"},
        "details": [{"factorKey": "pages_read", "value": 30}],
    }


def test_disabled_gateway_makes_no_http_call(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.read.infrastructure.integrations.logos_progression_gateway.urlopen",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("HTTP call")),
    )

    result = LogosProgressionGateway(
        LogosProgressionSettings(None, False, 5, None)
    ).evaluate_reading_session(ReadingProgressionFact("session", UserId.new(), 1))

    assert result.success is False
    assert result.error == "disabled"


def test_http_failure_is_reported_without_raising(monkeypatch) -> None:
    def fake_urlopen(*_args, **_kwargs):
        raise HTTPError("http://logos.test", 500, "failure", {}, None)

    monkeypatch.setattr(
        "app.read.infrastructure.integrations.logos_progression_gateway.urlopen",
        fake_urlopen,
    )
    gateway = LogosProgressionGateway(
        LogosProgressionSettings("http://logos.test", True, 5, "token")
    )

    result = gateway.evaluate_reading_session(
        ReadingProgressionFact("session", UserId.new(), 1)
    )

    assert result.success is False
    assert result.status_code == 500
    assert result.error == "http_error"

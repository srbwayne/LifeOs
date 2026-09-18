from app.read.dependencies import get_progression_gateway
from app.read.infrastructure.integrations.durable_progression_gateway import (
    DurableProgressionGateway,
)
from app.read.infrastructure.integrations.logos_progression_gateway import (
    LogosProgressionGateway,
)
from app.read.infrastructure.integrations.noop_progression_gateway import NoOpProgressionGateway


def test_disabled_logos_integration_keeps_noop_default(monkeypatch) -> None:
    monkeypatch.delenv("LIFEOS_LOGOS_PROGRESSION_ENABLED", raising=False)
    assert isinstance(get_progression_gateway(), NoOpProgressionGateway)


def test_enabled_logos_integration_composes_durable_gateway(monkeypatch) -> None:
    monkeypatch.setenv("LIFEOS_LOGOS_PROGRESSION_ENABLED", "true")
    monkeypatch.setenv("LIFEOS_LOGOS_BASE_URL", "https://logos.example")
    monkeypatch.setenv("LIFEOS_LOGOS_BEARER_TOKEN", "fake-token")
    monkeypatch.setenv("LIFEOS_LOGOS_READING_CONFIGURATION_KEY", "reading-v1")
    monkeypatch.setenv("LIFEOS_LOGOS_READING_CONFIGURATION_REVISION", "3")
    monkeypatch.setenv("LIFEOS_LOGOS_TIMEOUT_SECONDS", "2")

    gateway = get_progression_gateway()

    assert isinstance(gateway, DurableProgressionGateway)
    assert isinstance(gateway._dispatcher._downstream, LogosProgressionGateway)


def test_enabled_logos_integration_without_revision_fails_fast(monkeypatch) -> None:
    monkeypatch.setenv("LIFEOS_LOGOS_PROGRESSION_ENABLED", "true")
    monkeypatch.setenv("LIFEOS_LOGOS_BASE_URL", "https://logos.example")
    monkeypatch.setenv("LIFEOS_LOGOS_BEARER_TOKEN", "fake-token")
    monkeypatch.setenv("LIFEOS_LOGOS_READING_CONFIGURATION_KEY", "reading-v1")
    monkeypatch.setenv("LIFEOS_LOGOS_TIMEOUT_SECONDS", "2")
    monkeypatch.delenv("LIFEOS_LOGOS_READING_CONFIGURATION_REVISION", raising=False)

    try:
        get_progression_gateway()
    except ValueError as error:
        assert "LIFEOS_LOGOS_READING_CONFIGURATION_REVISION" in str(error)
    else:
        raise AssertionError("enabled configuration without revision must fail fast")


def test_enabled_invalid_logos_configuration_fails_fast(monkeypatch) -> None:
    monkeypatch.setenv("LIFEOS_LOGOS_PROGRESSION_ENABLED", "true")
    monkeypatch.delenv("LIFEOS_LOGOS_BASE_URL", raising=False)

    try:
        get_progression_gateway()
    except ValueError as error:
        assert "LIFEOS_LOGOS_BASE_URL" in str(error)
    else:
        raise AssertionError("enabled invalid configuration must fail fast")

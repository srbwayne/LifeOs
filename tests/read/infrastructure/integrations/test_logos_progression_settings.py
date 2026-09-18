import pytest

from app.read.infrastructure.integrations.logos_progression_settings import (
    LogosProgressionConfigurationError,
    LogosProgressionSettings,
)

_PREFIX = "LIFEOS_LOGOS_"


def _set_enabled_environment(monkeypatch) -> None:
    monkeypatch.setenv(f"{_PREFIX}PROGRESSION_ENABLED", "true")
    monkeypatch.setenv(f"{_PREFIX}BASE_URL", "https://logos.example")
    monkeypatch.setenv(f"{_PREFIX}BEARER_TOKEN", "fake-token")
    monkeypatch.setenv(f"{_PREFIX}READING_CONFIGURATION_KEY", "reading-v1")
    monkeypatch.setenv(f"{_PREFIX}READING_CONFIGURATION_REVISION", "3")
    monkeypatch.setenv(f"{_PREFIX}TIMEOUT_SECONDS", "2.5")


def test_absent_enabled_defaults_to_disabled(monkeypatch) -> None:
    monkeypatch.delenv("LIFEOS_LOGOS_PROGRESSION_ENABLED", raising=False)
    settings = LogosProgressionSettings.from_environment()
    assert settings == LogosProgressionSettings()


def test_explicit_false_does_not_require_other_settings(monkeypatch) -> None:
    monkeypatch.setenv("LIFEOS_LOGOS_PROGRESSION_ENABLED", "false")
    settings = LogosProgressionSettings.from_environment()
    assert settings.enabled is False


def test_valid_enabled_settings_are_parsed(monkeypatch) -> None:
    _set_enabled_environment(monkeypatch)
    settings = LogosProgressionSettings.from_environment()
    assert settings.enabled is True
    assert settings.base_url == "https://logos.example"
    assert settings.reading_configuration_revision == 3
    assert settings.timeout_seconds == 2.5


@pytest.mark.parametrize("value", ["yes", "1", "enabled", ""])
def test_invalid_enabled_boolean_fails(monkeypatch, value) -> None:
    monkeypatch.setenv("LIFEOS_LOGOS_PROGRESSION_ENABLED", value)
    with pytest.raises(LogosProgressionConfigurationError):
        LogosProgressionSettings.from_environment()


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("LIFEOS_LOGOS_BASE_URL", "not-a-url"),
        ("LIFEOS_LOGOS_BASE_URL", "ftp://logos.example"),
        ("LIFEOS_LOGOS_BEARER_TOKEN", ""),
        ("LIFEOS_LOGOS_READING_CONFIGURATION_KEY", " "),
        ("LIFEOS_LOGOS_TIMEOUT_SECONDS", "0"),
        ("LIFEOS_LOGOS_TIMEOUT_SECONDS", "-1"),
        ("LIFEOS_LOGOS_TIMEOUT_SECONDS", "NaN"),
        ("LIFEOS_LOGOS_TIMEOUT_SECONDS", "Infinity"),
        ("LIFEOS_LOGOS_TIMEOUT_SECONDS", "not-number"),
    ],
)
def test_invalid_required_setting_fails(monkeypatch, name, value) -> None:
    _set_enabled_environment(monkeypatch)
    monkeypatch.setenv(name, value)
    with pytest.raises(LogosProgressionConfigurationError):
        LogosProgressionSettings.from_environment()


@pytest.mark.parametrize(
    "name",
    [
        "LIFEOS_LOGOS_BASE_URL",
        "LIFEOS_LOGOS_BEARER_TOKEN",
        "LIFEOS_LOGOS_READING_CONFIGURATION_KEY",
        "LIFEOS_LOGOS_READING_CONFIGURATION_REVISION",
        "LIFEOS_LOGOS_TIMEOUT_SECONDS",
    ],
)
def test_missing_required_setting_fails(monkeypatch, name) -> None:
    _set_enabled_environment(monkeypatch)
    monkeypatch.delenv(name)
    with pytest.raises(LogosProgressionConfigurationError):
        LogosProgressionSettings.from_environment()


@pytest.mark.parametrize("value", ["0", "-1", "nope"])
def test_invalid_revision_fails(monkeypatch, value) -> None:
    _set_enabled_environment(monkeypatch)
    monkeypatch.setenv("LIFEOS_LOGOS_READING_CONFIGURATION_REVISION", value)
    with pytest.raises(LogosProgressionConfigurationError):
        LogosProgressionSettings.from_environment()


@pytest.mark.parametrize("value", ["", " "])
def test_blank_revision_fails(monkeypatch, value) -> None:
    _set_enabled_environment(monkeypatch)
    monkeypatch.setenv("LIFEOS_LOGOS_READING_CONFIGURATION_REVISION", value)
    with pytest.raises(LogosProgressionConfigurationError):
        LogosProgressionSettings.from_environment()


def test_token_is_not_exposed_by_repr_or_error(monkeypatch) -> None:
    _set_enabled_environment(monkeypatch)
    settings = LogosProgressionSettings.from_environment()
    assert "fake-token" not in repr(settings)
    assert "fake-token" not in str(settings)
    monkeypatch.setenv("LIFEOS_LOGOS_BASE_URL", "invalid")
    with pytest.raises(LogosProgressionConfigurationError) as error:
        LogosProgressionSettings.from_environment()
    assert "fake-token" not in str(error.value)

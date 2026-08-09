import pytest

from app.read.domain.value_objects.reading_session_id import ReadingSessionId


def test_reading_session_id_generation_produces_valid_canonical_tsid() -> None:
    session_id = ReadingSessionId.new()

    assert session_id.value
    assert ReadingSessionId.from_value(session_id.value) == session_id


def test_reading_session_id_restoration_preserves_persistence_and_string() -> None:
    created = ReadingSessionId.new()
    restored = ReadingSessionId.from_value(created.to_persistence())

    assert restored == created
    assert hash(restored) == hash(created)
    assert str(restored) == created.value
    assert restored.to_persistence() == created.value


@pytest.mark.parametrize("value", ["", "not-a-tsid"])
def test_reading_session_id_rejects_empty_or_invalid_value(value: str) -> None:
    with pytest.raises(ValueError):
        ReadingSessionId.from_value(value)


def test_reading_session_id_rejects_noncanonical_representation() -> None:
    canonical = ReadingSessionId.new().value
    noncanonical = canonical.lower()

    if noncanonical == canonical:
        pytest.skip("Generated TSID contains no alphabetic characters.")

    with pytest.raises(ValueError):
        ReadingSessionId.from_value(noncanonical)

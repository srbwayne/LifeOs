import pytest
from tsidpy import TSID

from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId


def test_therapy_session_id_generation_round_trips_through_persistence() -> None:
    identifier = TherapySessionId.new()

    assert identifier.value
    assert TSID.from_string(identifier.value).to_string() == identifier.value
    assert TherapySessionId.from_value(identifier.to_persistence()) == identifier
    assert str(identifier) == identifier.value
    assert hash(TherapySessionId.from_value(identifier.value)) == hash(identifier)


@pytest.mark.parametrize("value", ["", "not-a-tsid"])
def test_therapy_session_id_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        TherapySessionId.from_value(value)


def test_therapy_session_id_rejects_noncanonical_representation() -> None:
    canonical = TherapySessionId.new().value
    noncanonical = canonical.lower()

    if noncanonical == canonical:
        pytest.skip("Generated TSID contains no alphabetic characters.")

    with pytest.raises(ValueError):
        TherapySessionId.from_value(noncanonical)

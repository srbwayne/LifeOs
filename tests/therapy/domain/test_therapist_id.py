import pytest
from tsidpy import TSID

from app.therapy.domain.value_objects.therapist_id import TherapistId


def test_therapist_id_generation_round_trips_through_persistence() -> None:
    identifier = TherapistId.new()

    assert identifier.value
    assert TSID.from_string(identifier.value).to_string() == identifier.value
    assert TherapistId.from_value(identifier.to_persistence()) == identifier
    assert str(identifier) == identifier.value
    assert hash(TherapistId.from_value(identifier.value)) == hash(identifier)


@pytest.mark.parametrize("value", ["", "not-a-tsid"])
def test_therapist_id_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        TherapistId.from_value(value)


def test_therapist_id_rejects_noncanonical_representation() -> None:
    canonical = TherapistId.new().value
    noncanonical = canonical.lower()

    if noncanonical == canonical:
        pytest.skip("Generated TSID contains no alphabetic characters.")

    with pytest.raises(ValueError):
        TherapistId.from_value(noncanonical)

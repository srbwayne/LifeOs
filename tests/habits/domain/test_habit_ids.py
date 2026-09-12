from typing import cast

import pytest
from tsidpy import TSID

from app.habits.domain.value_objects.habit_completion_id import HabitCompletionId
from app.habits.domain.value_objects.habit_id import HabitId

IdentifierType = type[HabitId] | type[HabitCompletionId]


@pytest.mark.parametrize("identifier_type", [HabitId, HabitCompletionId])
def test_identifier_generation_and_persistence_round_trip(identifier_type: IdentifierType) -> None:
    identifier = identifier_type.new()

    assert identifier.value
    assert TSID.from_string(identifier.value).to_string() == identifier.value
    assert identifier_type.from_value(identifier.to_persistence()) == identifier
    assert str(identifier) == identifier.value


@pytest.mark.parametrize("identifier_type", [HabitId, HabitCompletionId])
@pytest.mark.parametrize("value", ["", "not-a-tsid", None, 42])
def test_identifier_rejects_empty_malformed_and_wrong_values(
    identifier_type: IdentifierType,
    value: object,
) -> None:
    with pytest.raises(ValueError):
        identifier_type.from_value(cast(str, value))


@pytest.mark.parametrize("identifier_type", [HabitId, HabitCompletionId])
def test_identifier_rejects_noncanonical_representation(identifier_type: IdentifierType) -> None:
    canonical = identifier_type.new().value
    noncanonical = canonical.lower()

    if noncanonical == canonical:
        pytest.skip("Generated TSID contains no alphabetic characters.")

    with pytest.raises(ValueError):
        identifier_type.from_value(noncanonical)

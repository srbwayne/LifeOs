import pytest

from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.errors.habit_errors import InvalidHabitNameError
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


def test_create_preserves_owner_normalizes_name_and_defaults_active() -> None:
    owner_id = UserId.new()

    habit = Habit.create(owner_id, "  Read a book  ")

    assert isinstance(habit.id, HabitId)
    assert habit.owner_id == owner_id
    assert habit.name == "Read a book"
    assert habit.description is None
    assert habit.active is True


def test_name_preserves_case_and_has_no_artificial_maximum() -> None:
    name = "A" * 1000

    habit = Habit.create(UserId.new(), f"  {name}  ")

    assert habit.name == name


@pytest.mark.parametrize("name", ["", "   ", None, 42])
def test_name_rejects_blank_and_non_string_values(name: object) -> None:
    with pytest.raises(InvalidHabitNameError):
        Habit.create(UserId.new(), name)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("description", "expected"),
    [(None, None), ("", None), ("   ", None), ("  Details  ", "Details")],
)
def test_description_normalization(description: str | None, expected: str | None) -> None:
    habit = Habit.create(UserId.new(), "Example", description)

    assert habit.description == expected


def test_description_rejects_non_string_values() -> None:
    with pytest.raises(TypeError):
        Habit.create(UserId.new(), "Example", 42)  # type: ignore[arg-type]


def test_lifecycle_is_idempotent() -> None:
    habit = Habit.create(UserId.new(), "Example")

    habit.deactivate()
    habit.deactivate()
    assert habit.active is False

    habit.activate()
    habit.activate()
    assert habit.active is True


def test_restore_preserves_identity_owner_state_and_normalizes_values() -> None:
    identifier = HabitId.new()
    owner_id = UserId.new()

    habit = Habit.restore(identifier, owner_id, "  Example  ", "  Details  ", False)

    assert habit.id == identifier
    assert habit.owner_id == owner_id
    assert habit.name == "Example"
    assert habit.description == "Details"
    assert habit.active is False


@pytest.mark.parametrize(
    ("identifier", "owner_id", "active"),
    [
        (object(), UserId.new(), True),
        (HabitId.new(), object(), True),
        (HabitId.new(), UserId.new(), 1),
    ],
)
def test_constructor_rejects_wrong_structural_types(
    identifier: object,
    owner_id: object,
    active: object,
) -> None:
    with pytest.raises(TypeError):
        Habit(identifier, owner_id, "Example", None, active)  # type: ignore[arg-type]


@pytest.mark.parametrize("attribute", ["id", "owner_id", "name", "description", "active"])
def test_structural_attributes_are_read_only(attribute: str) -> None:
    habit = Habit.create(UserId.new(), "Example")

    with pytest.raises(AttributeError):
        setattr(habit, attribute, object())


def test_equality_uses_identity_and_aggregate_is_unhashable() -> None:
    identifier = HabitId.new()
    owner_id = UserId.new()
    first = Habit.restore(identifier, owner_id, "First", None, True)
    same_identity = Habit.restore(identifier, UserId.new(), "Second", "Details", False)
    different_identity = Habit.create(owner_id, "First")

    assert first == same_identity
    assert first != different_identity
    with pytest.raises(TypeError):
        hash(first)


def test_habit_has_no_events_or_rename_delete_behavior() -> None:
    habit = Habit.create(UserId.new(), "Example")

    assert habit.domain_events == []
    assert not hasattr(habit, "rename")
    assert not hasattr(habit, "delete")

from datetime import date, datetime, timedelta

import pytest

from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.domain.value_objects.habit_completion_id import HabitCompletionId
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


def test_create_preserves_owner_habit_and_civil_date() -> None:
    owner_id = UserId.new()
    habit_id = HabitId.new()
    record_date = date(2020, 1, 2)

    completion = HabitCompletion.create(owner_id, habit_id, record_date)

    assert isinstance(completion.id, HabitCompletionId)
    assert completion.owner_id == owner_id
    assert completion.habit_id == habit_id
    assert completion.record_date == record_date
    assert completion.domain_events == []


def test_restore_preserves_identity_and_accepts_future_civil_date() -> None:
    identifier = HabitCompletionId.new()
    future = date.today() + timedelta(days=365)

    completion = HabitCompletion.restore(identifier, UserId.new(), HabitId.new(), future)

    assert completion.id == identifier
    assert completion.record_date == future


@pytest.mark.parametrize("record_date", [datetime(2026, 9, 12), "2026-09-12", 42, None])
def test_record_date_rejects_datetime_and_non_date_values(record_date: object) -> None:
    with pytest.raises(TypeError):
        HabitCompletion.create(UserId.new(), HabitId.new(), record_date)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("identifier", "owner_id", "habit_id"),
    [
        (object(), UserId.new(), HabitId.new()),
        (HabitCompletionId.new(), object(), HabitId.new()),
        (HabitCompletionId.new(), UserId.new(), object()),
    ],
)
def test_constructor_rejects_wrong_structural_types(
    identifier: object,
    owner_id: object,
    habit_id: object,
) -> None:
    with pytest.raises(TypeError):
        HabitCompletion(identifier, owner_id, habit_id, date(2026, 9, 12))  # type: ignore[arg-type]


@pytest.mark.parametrize("attribute", ["id", "owner_id", "habit_id", "record_date"])
def test_structural_attributes_are_read_only(attribute: str) -> None:
    completion = HabitCompletion.create(UserId.new(), HabitId.new(), date(2026, 9, 12))

    with pytest.raises(AttributeError):
        setattr(completion, attribute, object())


def test_equality_uses_identity_and_aggregate_is_unhashable() -> None:
    identifier = HabitCompletionId.new()
    first = HabitCompletion.restore(identifier, UserId.new(), HabitId.new(), date(2026, 9, 12))
    same_identity = HabitCompletion.restore(
        identifier, UserId.new(), HabitId.new(), date(2020, 1, 1)
    )
    different_identity = HabitCompletion.create(UserId.new(), HabitId.new(), date(2026, 9, 12))

    assert first == same_identity
    assert first != different_identity
    with pytest.raises(TypeError):
        hash(first)


def test_completion_has_no_mutation_or_business_fields() -> None:
    completion = HabitCompletion.create(UserId.new(), HabitId.new(), date(2026, 9, 12))

    assert not hasattr(completion, "complete")
    assert not hasattr(completion, "uncomplete")
    assert not hasattr(completion, "created_at")
    assert not hasattr(completion, "completed")

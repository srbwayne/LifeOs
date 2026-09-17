from collections.abc import Collection
from datetime import date

from app.habits.application.queries.get_habit_streak import (
    GetHabitStreakQuery,
    GetHabitStreakQueryHandler,
)
from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.services.current_habit_streak import CurrentHabitStreakCalculator
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


class HabitRepositoryFake:
    def __init__(self, habit: Habit | None) -> None:
        self.habit = habit
        self.calls: list[tuple[HabitId, UserId]] = []

    def save(self, habit: Habit) -> None:
        self.habit = habit

    def get_by_id_and_owner(self, habit_id: HabitId, owner_id: UserId) -> Habit | None:
        self.calls.append((habit_id, owner_id))
        if self.habit and self.habit.id == habit_id and self.habit.owner_id == owner_id:
            return self.habit
        return None

    def get_by_owner_and_name(self, owner_id: UserId, name: str) -> Habit | None:
        return None


class CompletionReadRepositoryFake:
    def __init__(self, dates: tuple[date, ...]) -> None:
        self.dates = dates
        self.calls: list[tuple[UserId, HabitId, date]] = []

    def list_by_owner_and_habit(self, owner_id: UserId, habit_id: HabitId, page: int, size: int):
        raise AssertionError("legacy completion list must not be used")

    def list_record_dates_by_owner_and_habit_until(
        self, owner_id: UserId, habit_id: HabitId, evaluation_date: date
    ) -> tuple[date, ...]:
        self.calls.append((owner_id, habit_id, evaluation_date))
        return self.dates


class RecordingCalculator(CurrentHabitStreakCalculator):
    def __init__(self) -> None:
        self.calls: list[tuple[date, tuple[date, ...]]] = []

    def calculate(self, evaluation_date: date, completion_dates: Collection[date]) -> int:
        self.calls.append((evaluation_date, tuple(completion_dates)))
        return 7


def test_active_habit_uses_one_owner_scoped_projection_and_calculator() -> None:
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Read")
    evaluation_date = date(2026, 9, 14)
    repository = HabitRepositoryFake(habit)
    completion_repository = CompletionReadRepositoryFake((evaluation_date,))
    calculator = RecordingCalculator()

    result = GetHabitStreakQueryHandler(repository, completion_repository, calculator)(
        GetHabitStreakQuery(owner_id, habit.id, evaluation_date)
    )

    assert result.habit_id == habit.id.value
    assert result.current_streak == 7
    assert result.evaluation_date == evaluation_date
    assert repository.calls == [(habit.id, owner_id)]
    assert completion_repository.calls == [(owner_id, habit.id, evaluation_date)]
    assert calculator.calls == [(evaluation_date, (evaluation_date,))]


def test_inactive_habit_returns_none_without_completion_projection() -> None:
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Read")
    habit.deactivate()
    repository = HabitRepositoryFake(habit)
    completion_repository = CompletionReadRepositoryFake(())
    calculator = RecordingCalculator()

    result = GetHabitStreakQueryHandler(repository, completion_repository, calculator)(
        GetHabitStreakQuery(owner_id, habit.id, date(2026, 9, 14))
    )

    assert result.current_streak is None
    assert completion_repository.calls == []
    assert calculator.calls == []


def test_missing_or_foreign_habit_has_same_not_found_behavior() -> None:
    from app.habits.application.errors.habit_errors import HabitNotFoundError

    owner_id = UserId.new()
    stored_habit = Habit.create(owner_id, "Read")
    handler = GetHabitStreakQueryHandler(
        HabitRepositoryFake(stored_habit),
        CompletionReadRepositoryFake(()),
        CurrentHabitStreakCalculator(),
    )

    for query in (
        GetHabitStreakQuery(owner_id, HabitId.new(), date(2026, 9, 14)),
        GetHabitStreakQuery(UserId.new(), stored_habit.id, date(2026, 9, 14)),
    ):
        try:
            handler(query)
        except HabitNotFoundError:
            pass
        else:
            raise AssertionError("expected HabitNotFoundError")

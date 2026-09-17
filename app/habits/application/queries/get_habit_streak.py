from dataclasses import dataclass
from datetime import date

from app.habits.application.dtos.habit_streak_dto import HabitStreakDTO
from app.habits.application.errors.habit_errors import HabitNotFoundError
from app.habits.application.ports.habit_completion_read_repository import (
    IHabitCompletionReadRepository,
)
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.domain.services.current_habit_streak import CurrentHabitStreakCalculator
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class GetHabitStreakQuery:
    owner_id: UserId
    habit_id: HabitId
    evaluation_date: date


class GetHabitStreakQueryHandler:
    def __init__(
        self,
        habit_repository: IHabitRepository,
        completion_read_repository: IHabitCompletionReadRepository,
        calculator: CurrentHabitStreakCalculator,
    ) -> None:
        self._habits = habit_repository
        self._completions = completion_read_repository
        self._calculator = calculator

    def __call__(self, query: GetHabitStreakQuery) -> HabitStreakDTO:
        habit = self._habits.get_by_id_and_owner(query.habit_id, query.owner_id)
        if habit is None:
            raise HabitNotFoundError()
        if not habit.active:
            return HabitStreakDTO(habit.id.value, None, query.evaluation_date)

        completion_dates = self._completions.list_record_dates_by_owner_and_habit_until(
            query.owner_id,
            query.habit_id,
            query.evaluation_date,
        )
        current_streak = self._calculator.calculate(
            query.evaluation_date,
            completion_dates,
        )
        return HabitStreakDTO(habit.id.value, current_streak, query.evaluation_date)

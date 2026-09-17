from datetime import date
from typing import Protocol

from app.habits.application.dtos.habit_completion_dto import HabitCompletionPageDTO
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


class IHabitCompletionReadRepository(Protocol):
    def list_by_owner_and_habit(
        self,
        owner_id: UserId,
        habit_id: HabitId,
        page: int,
        size: int,
    ) -> HabitCompletionPageDTO: ...

    def list_record_dates_by_owner_and_habit_until(
        self,
        owner_id: UserId,
        habit_id: HabitId,
        evaluation_date: date,
    ) -> tuple[date, ...]: ...

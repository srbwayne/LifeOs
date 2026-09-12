from datetime import date
from typing import Protocol

from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


class IHabitCompletionRepository(Protocol):
    def save(self, completion: HabitCompletion) -> None: ...

    def get_by_owner_habit_date(
        self,
        owner_id: UserId,
        habit_id: HabitId,
        record_date: date,
    ) -> HabitCompletion | None: ...

    def delete(self, completion: HabitCompletion) -> None: ...

from typing import Protocol

from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


class IHabitRepository(Protocol):
    def save(self, habit: Habit) -> None: ...

    def get_by_id_and_owner(
        self,
        habit_id: HabitId,
        owner_id: UserId,
    ) -> Habit | None: ...

    def get_by_owner_and_name(
        self,
        owner_id: UserId,
        name: str,
    ) -> Habit | None: ...

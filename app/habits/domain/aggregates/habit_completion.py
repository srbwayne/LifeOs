from __future__ import annotations

from datetime import date, datetime

from app.habits.domain.value_objects.habit_completion_id import HabitCompletionId
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId


class HabitCompletion(AggregateRoot):
    """Immutable owner-scoped civil-date completion fact."""

    def __init__(
        self,
        id: HabitCompletionId,
        owner_id: UserId,
        habit_id: HabitId,
        record_date: date,
    ) -> None:
        super().__init__()
        if not isinstance(id, HabitCompletionId):
            raise TypeError("Habit completion ID must be a HabitCompletionId.")
        if not isinstance(owner_id, UserId):
            raise TypeError("Habit completion owner must be a UserId.")
        if not isinstance(habit_id, HabitId):
            raise TypeError("Habit completion Habit ID must be a HabitId.")
        if isinstance(record_date, datetime) or not isinstance(record_date, date):
            raise TypeError("Habit completion record date must be a date.")
        self._id = id
        self._owner_id = owner_id
        self._habit_id = habit_id
        self._record_date = record_date

    @classmethod
    def create(
        cls,
        owner_id: UserId,
        habit_id: HabitId,
        record_date: date,
    ) -> HabitCompletion:
        return cls(HabitCompletionId.new(), owner_id, habit_id, record_date)

    @classmethod
    def restore(
        cls,
        id: HabitCompletionId,
        owner_id: UserId,
        habit_id: HabitId,
        record_date: date,
    ) -> HabitCompletion:
        return cls(id, owner_id, habit_id, record_date)

    @property
    def id(self) -> HabitCompletionId:
        return self._id

    @property
    def owner_id(self) -> UserId:
        return self._owner_id

    @property
    def habit_id(self) -> HabitId:
        return self._habit_id

    @property
    def record_date(self) -> date:
        return self._record_date

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HabitCompletion):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'HabitCompletion'")

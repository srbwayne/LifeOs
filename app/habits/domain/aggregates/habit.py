from __future__ import annotations

from app.habits.domain.errors.habit_errors import InvalidHabitNameError
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId


class Habit(AggregateRoot):
    """Owner-scoped reusable Habit aggregate root."""

    def __init__(
        self,
        id: HabitId,
        owner_id: UserId,
        name: str,
        description: str | None,
        active: bool,
    ) -> None:
        super().__init__()
        if not isinstance(id, HabitId):
            raise TypeError("Habit ID must be a HabitId.")
        if not isinstance(owner_id, UserId):
            raise TypeError("Habit owner must be a UserId.")
        if not isinstance(active, bool):
            raise TypeError("Habit active must be a bool.")
        self._id = id
        self._owner_id = owner_id
        self._name = self._normalize_name(name)
        self._description = self._normalize_description(description)
        self._active = active

    @classmethod
    def create(
        cls,
        owner_id: UserId,
        name: str,
        description: str | None = None,
    ) -> Habit:
        return cls(HabitId.new(), owner_id, name, description, True)

    @classmethod
    def restore(
        cls,
        id: HabitId,
        owner_id: UserId,
        name: str,
        description: str | None,
        active: bool,
    ) -> Habit:
        return cls(id, owner_id, name, description, active)

    @staticmethod
    def _normalize_name(value: str) -> str:
        if not isinstance(value, str) or not (normalized := value.strip()):
            raise InvalidHabitNameError()
        return normalized

    @staticmethod
    def _normalize_description(value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("Habit description must be a string or None.")
        normalized = value.strip()
        return normalized or None

    @property
    def id(self) -> HabitId:
        return self._id

    @property
    def owner_id(self) -> UserId:
        return self._owner_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def active(self) -> bool:
        return self._active

    def deactivate(self) -> None:
        self._active = False

    def activate(self) -> None:
        self._active = True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Habit):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'Habit'")

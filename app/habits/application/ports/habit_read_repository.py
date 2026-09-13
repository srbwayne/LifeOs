from typing import Protocol

from app.habits.application.dtos.habit_dto import HabitDTO
from app.shared.domain.identifiers.user_id import UserId


class IHabitReadRepository(Protocol):
    def list_by_owner(self, owner_id: UserId) -> tuple[HabitDTO, ...]: ...

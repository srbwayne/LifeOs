from datetime import date
from typing import Protocol

from app.habits.application.dtos.habit_checklist_dto import HabitChecklistItemDTO
from app.habits.application.dtos.habit_dto import HabitDTO
from app.shared.domain.identifiers.user_id import UserId


class IHabitReadRepository(Protocol):
    def list_by_owner(self, owner_id: UserId) -> tuple[HabitDTO, ...]: ...

    def get_checklist_by_owner_and_record_date(
        self, owner_id: UserId, record_date: date
    ) -> tuple[HabitChecklistItemDTO, ...]: ...

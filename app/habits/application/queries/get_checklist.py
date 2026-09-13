from dataclasses import dataclass
from datetime import date

from app.habits.application.dtos.habit_checklist_dto import HabitChecklistItemDTO
from app.habits.application.ports.habit_read_repository import IHabitReadRepository
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class GetChecklistQuery:
    owner_id: UserId
    record_date: date


class GetChecklistQueryHandler:
    def __init__(self, repository: IHabitReadRepository) -> None:
        self._repository = repository

    def __call__(self, query: GetChecklistQuery) -> tuple[HabitChecklistItemDTO, ...]:
        return self._repository.get_checklist_by_owner_and_record_date(
            query.owner_id, query.record_date
        )

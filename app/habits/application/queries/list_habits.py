from dataclasses import dataclass

from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.ports.habit_read_repository import IHabitReadRepository
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ListHabitsQuery:
    owner_id: UserId


class ListHabitsQueryHandler:
    def __init__(self, repository: IHabitReadRepository) -> None:
        self._repository = repository

    def __call__(self, query: ListHabitsQuery) -> tuple[HabitDTO, ...]:
        return self._repository.list_by_owner(query.owner_id)

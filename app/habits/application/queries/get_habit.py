from dataclasses import dataclass

from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.errors.habit_errors import HabitNotFoundError
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class GetHabitQuery:
    owner_id: UserId
    habit_id: HabitId


class GetHabitQueryHandler:
    def __init__(self, repository: IHabitRepository) -> None:
        self._repository = repository

    def __call__(self, query: GetHabitQuery) -> HabitDTO:
        habit = self._repository.get_by_id_and_owner(query.habit_id, query.owner_id)
        if habit is None:
            raise HabitNotFoundError()
        return HabitDTO(habit.id.value, habit.name, habit.description, habit.active)

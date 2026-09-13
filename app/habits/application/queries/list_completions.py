from dataclasses import dataclass

from app.habits.application.dtos.habit_completion_dto import HabitCompletionPageDTO
from app.habits.application.errors.habit_errors import HabitNotFoundError
from app.habits.application.ports.habit_completion_read_repository import (
    IHabitCompletionReadRepository,
)
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ListCompletionsQuery:
    owner_id: UserId
    habit_id: HabitId
    page: int
    size: int


class ListCompletionsQueryHandler:
    def __init__(
        self,
        habit_repository: IHabitRepository,
        completion_read_repository: IHabitCompletionReadRepository,
    ) -> None:
        self._habits = habit_repository
        self._completions = completion_read_repository

    def __call__(self, query: ListCompletionsQuery) -> HabitCompletionPageDTO:
        habit = self._habits.get_by_id_and_owner(query.habit_id, query.owner_id)
        if habit is None:
            raise HabitNotFoundError()
        return self._completions.list_by_owner_and_habit(
            query.owner_id,
            query.habit_id,
            query.page,
            query.size,
        )

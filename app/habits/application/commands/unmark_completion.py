from dataclasses import dataclass
from datetime import date

from app.habits.application.errors.habit_errors import (
    HabitCompletionNotFoundError,
    HabitNotFoundError,
)
from app.habits.domain.ports.habit_completion_repository import (
    IHabitCompletionRepository,
)
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class UnmarkCompletionCommand:
    owner_id: UserId
    habit_id: HabitId
    record_date: date


class UnmarkCompletionCommandHandler:
    def __init__(
        self,
        habit_repository: IHabitRepository,
        completion_repository: IHabitCompletionRepository,
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._habits = habit_repository
        self._completions = completion_repository
        self._uow = unit_of_work

    def __call__(self, command: UnmarkCompletionCommand) -> None:
        with self._uow as uow:
            habit = self._habits.get_by_id_and_owner(command.habit_id, command.owner_id)
            if habit is None:
                raise HabitNotFoundError()

            completion = self._completions.get_by_owner_habit_date(
                command.owner_id,
                command.habit_id,
                command.record_date,
            )
            if completion is None:
                raise HabitCompletionNotFoundError()

            self._completions.delete(completion)
            uow.commit()

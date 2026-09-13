from dataclasses import dataclass
from datetime import date

from sqlalchemy.exc import IntegrityError

from app.habits.application.dtos.habit_completion_dto import HabitCompletionDTO
from app.habits.application.errors.habit_errors import (
    HabitNotFoundError,
    InactiveHabitError,
)
from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.domain.ports.habit_completion_repository import (
    IHabitCompletionRepository,
)
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class MarkCompletionCommand:
    owner_id: UserId
    habit_id: HabitId
    record_date: date


@dataclass(frozen=True)
class MarkCompletionResult:
    completion: HabitCompletionDTO
    created: bool


def _to_dto(completion: HabitCompletion) -> HabitCompletionDTO:
    return HabitCompletionDTO(
        id=completion.id.value,
        habit_id=completion.habit_id.value,
        record_date=completion.record_date,
    )


class MarkCompletionCommandHandler:
    def __init__(
        self,
        habit_repository: IHabitRepository,
        completion_repository: IHabitCompletionRepository,
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._habits = habit_repository
        self._completions = completion_repository
        self._uow = unit_of_work

    def __call__(self, command: MarkCompletionCommand) -> MarkCompletionResult:
        with self._uow as uow:
            habit = self._habits.get_by_id_and_owner(command.habit_id, command.owner_id)
            if habit is None:
                raise HabitNotFoundError()

            existing = self._completions.get_by_owner_habit_date(
                command.owner_id,
                command.habit_id,
                command.record_date,
            )
            if existing is not None:
                uow.commit()
                return MarkCompletionResult(_to_dto(existing), created=False)

            if not habit.active:
                raise InactiveHabitError()

            completion = HabitCompletion.create(
                owner_id=command.owner_id,
                habit_id=command.habit_id,
                record_date=command.record_date,
            )
            self._completions.save(completion)
            try:
                uow.flush()
            except IntegrityError as integrity_error:
                uow.rollback()
                winner = self._completions.get_by_owner_habit_date(
                    command.owner_id,
                    command.habit_id,
                    command.record_date,
                )
                if winner is None:
                    raise integrity_error
                uow.commit()
                return MarkCompletionResult(_to_dto(winner), created=False)

            uow.commit()
            return MarkCompletionResult(_to_dto(completion), created=True)

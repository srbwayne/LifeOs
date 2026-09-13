from dataclasses import dataclass

from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.errors.habit_errors import HabitNotFoundError
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ReactivateHabitCommand:
    owner_id: UserId
    habit_id: HabitId


class ReactivateHabitCommandHandler:
    def __init__(self, repository: IHabitRepository, unit_of_work: IUnitOfWork) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: ReactivateHabitCommand) -> HabitDTO:
        with self._unit_of_work as uow:
            habit = self._repository.get_by_id_and_owner(command.habit_id, command.owner_id)
            if habit is None:
                raise HabitNotFoundError()
            habit.activate()
            self._repository.save(habit)
            uow.commit()
        return HabitDTO(habit.id.value, habit.name, habit.description, habit.active)

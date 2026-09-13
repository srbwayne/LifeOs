from dataclasses import dataclass

from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.errors.habit_errors import HabitAlreadyExistsError
from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class CreateHabitCommand:
    owner_id: UserId
    name: str
    description: str | None = None


class CreateHabitCommandHandler:
    def __init__(self, repository: IHabitRepository, unit_of_work: IUnitOfWork) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: CreateHabitCommand) -> HabitDTO:
        with self._unit_of_work as uow:
            habit = Habit.create(
                owner_id=command.owner_id,
                name=command.name,
                description=command.description,
            )
            existing = self._repository.get_by_owner_and_name(command.owner_id, habit.name)
            if existing is not None:
                raise HabitAlreadyExistsError()
            self._repository.save(habit)
            uow.commit()
        return HabitDTO(habit.id.value, habit.name, habit.description, habit.active)

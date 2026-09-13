# ruff: noqa: B008

from fastapi import Depends
from sqlalchemy.orm import Session

from app.habits.application.commands.create_habit import CreateHabitCommandHandler
from app.habits.application.commands.deactivate_habit import DeactivateHabitCommandHandler
from app.habits.application.commands.reactivate_habit import ReactivateHabitCommandHandler
from app.habits.application.ports.habit_read_repository import IHabitReadRepository
from app.habits.application.queries.get_habit import GetHabitQueryHandler
from app.habits.application.queries.list_habits import ListHabitsQueryHandler
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.infrastructure.persistence.repositories.habit_read_repository import (
    SqlAlchemyHabitReadRepository,
)
from app.habits.infrastructure.persistence.repositories.habit_repository import (
    SqlAlchemyHabitRepository,
)
from app.shared.application.event_bus import IEventBus, InMemoryEventBus
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.infrastructure.database import get_db
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def get_habit_repository(db: Session = Depends(get_db)) -> IHabitRepository:
    return SqlAlchemyHabitRepository(db)


def get_habit_read_repository(db: Session = Depends(get_db)) -> IHabitReadRepository:
    return SqlAlchemyHabitReadRepository(db)


def get_habit_event_bus() -> IEventBus:
    return InMemoryEventBus()


def get_habit_uow(
    db: Session = Depends(get_db),
    event_bus: IEventBus = Depends(get_habit_event_bus),
) -> IUnitOfWork:
    return SqlAlchemyUnitOfWork(db, event_bus)


def get_create_habit_handler(
    repository: IHabitRepository = Depends(get_habit_repository),
    unit_of_work: IUnitOfWork = Depends(get_habit_uow),
) -> CreateHabitCommandHandler:
    return CreateHabitCommandHandler(repository, unit_of_work)


def get_get_habit_handler(
    repository: IHabitRepository = Depends(get_habit_repository),
) -> GetHabitQueryHandler:
    return GetHabitQueryHandler(repository)


def get_list_habits_handler(
    repository: IHabitReadRepository = Depends(get_habit_read_repository),
) -> ListHabitsQueryHandler:
    return ListHabitsQueryHandler(repository)


def get_deactivate_habit_handler(
    repository: IHabitRepository = Depends(get_habit_repository),
    unit_of_work: IUnitOfWork = Depends(get_habit_uow),
) -> DeactivateHabitCommandHandler:
    return DeactivateHabitCommandHandler(repository, unit_of_work)


def get_reactivate_habit_handler(
    repository: IHabitRepository = Depends(get_habit_repository),
    unit_of_work: IUnitOfWork = Depends(get_habit_uow),
) -> ReactivateHabitCommandHandler:
    return ReactivateHabitCommandHandler(repository, unit_of_work)

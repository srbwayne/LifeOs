# ruff: noqa: B008

from fastapi import Depends
from sqlalchemy.orm import Session

from app.habits.application.commands.create_habit import CreateHabitCommandHandler
from app.habits.application.commands.deactivate_habit import DeactivateHabitCommandHandler
from app.habits.application.commands.mark_completion import MarkCompletionCommandHandler
from app.habits.application.commands.reactivate_habit import ReactivateHabitCommandHandler
from app.habits.application.commands.unmark_completion import UnmarkCompletionCommandHandler
from app.habits.application.ports.habit_completion_read_repository import (
    IHabitCompletionReadRepository,
)
from app.habits.application.ports.habit_read_repository import IHabitReadRepository
from app.habits.application.queries.get_checklist import GetChecklistQueryHandler
from app.habits.application.queries.get_habit import GetHabitQueryHandler
from app.habits.application.queries.list_completions import ListCompletionsQueryHandler
from app.habits.application.queries.list_habits import ListHabitsQueryHandler
from app.habits.domain.ports.habit_completion_repository import IHabitCompletionRepository
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.infrastructure.persistence.repositories.habit_completion_read_repository import (
    SqlAlchemyHabitCompletionReadRepository,
)
from app.habits.infrastructure.persistence.repositories.habit_completion_repository import (
    SqlAlchemyHabitCompletionRepository,
)
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


def get_habit_completion_repository(
    db: Session = Depends(get_db),
) -> IHabitCompletionRepository:
    return SqlAlchemyHabitCompletionRepository(db)


def get_habit_completion_read_repository(
    db: Session = Depends(get_db),
) -> IHabitCompletionReadRepository:
    return SqlAlchemyHabitCompletionReadRepository(db)


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


def get_mark_completion_handler(
    habit_repository: IHabitRepository = Depends(get_habit_repository),
    completion_repository: IHabitCompletionRepository = Depends(get_habit_completion_repository),
    unit_of_work: IUnitOfWork = Depends(get_habit_uow),
) -> MarkCompletionCommandHandler:
    return MarkCompletionCommandHandler(habit_repository, completion_repository, unit_of_work)


def get_unmark_completion_handler(
    habit_repository: IHabitRepository = Depends(get_habit_repository),
    completion_repository: IHabitCompletionRepository = Depends(get_habit_completion_repository),
    unit_of_work: IUnitOfWork = Depends(get_habit_uow),
) -> UnmarkCompletionCommandHandler:
    return UnmarkCompletionCommandHandler(habit_repository, completion_repository, unit_of_work)


def get_get_checklist_handler(
    repository: IHabitReadRepository = Depends(get_habit_read_repository),
) -> GetChecklistQueryHandler:
    return GetChecklistQueryHandler(repository)


def get_list_completions_handler(
    habit_repository: IHabitRepository = Depends(get_habit_repository),
    completion_read_repository: IHabitCompletionReadRepository = Depends(
        get_habit_completion_read_repository
    ),
) -> ListCompletionsQueryHandler:
    return ListCompletionsQueryHandler(habit_repository, completion_read_repository)

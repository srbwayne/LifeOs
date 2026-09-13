from collections.abc import Iterator
from datetime import date, datetime
from threading import Barrier, Lock, Thread

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.habits.application.commands.mark_completion import (
    MarkCompletionCommand,
    MarkCompletionCommandHandler,
)
from app.habits.application.errors.habit_errors import InactiveHabitError
from app.habits.domain.aggregates.habit import Habit
from app.habits.infrastructure.persistence.models.habit_completion_model import (
    HabitCompletionModel,
)
from app.habits.infrastructure.persistence.repositories.habit_completion_repository import (
    SqlAlchemyHabitCompletionRepository,
)
from app.habits.infrastructure.persistence.repositories.habit_repository import (
    SqlAlchemyHabitRepository,
)
from app.shared.application.event_bus import InMemoryEventBus
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


@pytest.fixture
def completion_database(tmp_path) -> Iterator[sessionmaker[Session]]:
    engine = create_engine(
        f"sqlite:///{(tmp_path / 'habits-completion-race.db').resolve()}",
        connect_args={"check_same_thread": False, "timeout": 30},
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        yield factory
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def seed(factory: sessionmaker[Session]) -> tuple[UserId, Habit]:
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Race")
    now = datetime.now()
    with factory() as session:
        session.add(
            UserModel(
                id=owner_id.value,
                email=f"{owner_id.value}@race.test",
                hashed_password="hash",
                created_at=now,
                updated_at=now,
            )
        )
        SqlAlchemyHabitRepository(session).save(habit)
        session.commit()
    return owner_id, habit


def install_initial_lookup_barrier(
    repository: SqlAlchemyHabitCompletionRepository, barrier: Barrier
) -> None:
    original = repository.get_by_owner_habit_date
    calls = 0
    lock = Lock()

    def synchronized_lookup(owner_id, habit_id, record_date):
        nonlocal calls
        with lock:
            calls += 1
            initial_lookup = calls == 1
        if initial_lookup:
            barrier.wait(timeout=30)
        return original(owner_id, habit_id, record_date)

    repository.get_by_owner_habit_date = synchronized_lookup  # type: ignore[method-assign]


def test_mark_completion_two_sessions_recover_unique_race(
    completion_database: sessionmaker[Session],
) -> None:
    owner_id, habit = seed(completion_database)
    record_date = date(2026, 7, 7)
    barrier = Barrier(2)
    results = []
    errors: list[BaseException] = []
    result_lock = Lock()

    def worker() -> None:
        with completion_database() as session:
            habits = SqlAlchemyHabitRepository(session)
            completions = SqlAlchemyHabitCompletionRepository(session)
            install_initial_lookup_barrier(completions, barrier)
            handler = MarkCompletionCommandHandler(
                habits,
                completions,
                SqlAlchemyUnitOfWork(session, InMemoryEventBus()),
            )
            try:
                result = handler(MarkCompletionCommand(owner_id, habit.id, record_date))
                with result_lock:
                    results.append(result)
            except BaseException as exc:
                with result_lock:
                    errors.append(exc)

    threads = [Thread(target=worker), Thread(target=worker)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=45)

    assert not errors
    assert len(results) == 2
    assert sorted(result.created for result in results) == [False, True]
    assert len({result.completion.id for result in results}) == 1
    with completion_database() as session:
        rows = session.scalar(
            select(func.count(HabitCompletionModel.id)).where(
                HabitCompletionModel.user_id == owner_id.value,
                HabitCompletionModel.habit_id == habit.id.value,
                HabitCompletionModel.record_date == record_date,
            )
        )
        persisted = session.scalar(
            select(HabitCompletionModel).where(
                HabitCompletionModel.user_id == owner_id.value,
                HabitCompletionModel.habit_id == habit.id.value,
                HabitCompletionModel.record_date == record_date,
            )
        )
    assert rows == 1
    assert persisted is not None
    assert persisted.id == results[0].completion.id == results[1].completion.id


def test_mark_completion_inactive_new_date_remains_rejected(
    completion_database: sessionmaker[Session],
) -> None:
    owner_id, habit = seed(completion_database)
    with completion_database() as session:
        habit.deactivate()
        SqlAlchemyHabitRepository(session).save(habit)
        session.commit()
        handler = MarkCompletionCommandHandler(
            SqlAlchemyHabitRepository(session),
            SqlAlchemyHabitCompletionRepository(session),
            SqlAlchemyUnitOfWork(session, InMemoryEventBus()),
        )
        with pytest.raises(InactiveHabitError):
            handler(MarkCompletionCommand(owner_id, habit.id, date(2026, 8, 8)))

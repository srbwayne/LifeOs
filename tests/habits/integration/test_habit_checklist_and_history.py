from collections.abc import Iterator
from datetime import date, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.habits.application.dtos.habit_checklist_dto import HabitChecklistItemDTO
from app.habits.application.dtos.habit_completion_dto import HabitCompletionDTO
from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.infrastructure.persistence.models.habit_completion_model import (
    HabitCompletionModel,
)
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
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base


@pytest.fixture
def session(tmp_path) -> Iterator[Session]:
    engine = create_engine(f"sqlite:///{(tmp_path / 'habits-read-models.db').resolve()}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with factory() as db:
        yield db
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, owner_id: UserId) -> None:
    now = datetime.now()
    session.add(
        UserModel(
            id=owner_id.value,
            email=f"{owner_id.value}@read-model.test",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )


def add_habit(session: Session, owner_id: UserId, name: str, active: bool = True) -> Habit:
    habit = Habit.create(owner_id, name, "  Description  ")
    if not active:
        habit.deactivate()
    SqlAlchemyHabitRepository(session).save(habit)
    session.flush()
    return habit


def add_completion(
    session: Session, owner_id: UserId, habit: Habit, record_date: date
) -> HabitCompletion:
    completion = HabitCompletion.create(owner_id, habit.id, record_date)
    SqlAlchemyHabitCompletionRepository(session).save(completion)
    session.flush()
    return completion


def test_checklist_projects_current_active_habits_and_exact_date(session: Session) -> None:
    owner_id = UserId.new()
    other_owner = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner)
    active_completed = add_habit(session, owner_id, "Completed")
    add_habit(session, owner_id, "Empty")
    active_other_date = add_habit(session, owner_id, "Other date")
    inactive = add_habit(session, owner_id, "Inactive", active=False)
    other_habit = add_habit(session, other_owner, "Foreign")
    requested = date(2025, 1, 1)
    add_completion(session, owner_id, active_completed, requested)
    add_completion(session, owner_id, active_other_date, requested + timedelta(days=1))
    add_completion(session, owner_id, inactive, requested)
    add_completion(session, other_owner, other_habit, requested)

    result = SqlAlchemyHabitReadRepository(session).get_checklist_by_owner_and_record_date(
        owner_id, requested
    )

    assert all(isinstance(item, HabitChecklistItemDTO) for item in result)
    assert [(item.name, item.completed, item.description) for item in result] == [
        ("Completed", True, "Description"),
        ("Empty", False, "Description"),
        ("Other date", False, "Description"),
    ]
    assert inactive.name not in {item.name for item in result}


def test_checklist_historical_and_future_dates_do_not_create_rows(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    habit = add_habit(session, owner_id, "Current")
    repository = SqlAlchemyHabitReadRepository(session)

    historical = repository.get_checklist_by_owner_and_record_date(owner_id, date(2020, 1, 1))
    future = repository.get_checklist_by_owner_and_record_date(owner_id, date(2030, 1, 1))

    assert historical[0].completed is False
    assert future[0].completed is False
    assert session.query(HabitCompletionModel).count() == 0
    assert habit.active is True


def test_checklist_with_no_active_habits_is_empty(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    add_habit(session, owner_id, "Inactive", active=False)

    assert (
        SqlAlchemyHabitReadRepository(session).get_checklist_by_owner_and_record_date(
            owner_id, date(2026, 1, 1)
        )
        == ()
    )


def test_completion_history_is_owner_scoped_ordered_and_paginated(session: Session) -> None:
    owner_id = UserId.new()
    other_owner = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner)
    habit = add_habit(session, owner_id, "History", active=False)
    other_habit = add_habit(session, owner_id, "Other habit")
    foreign_habit = add_habit(session, other_owner, "Foreign")
    stored = [
        add_completion(session, owner_id, habit, date(2026, 1, 1) + timedelta(days=index))
        for index in range(5)
    ]
    add_completion(session, owner_id, other_habit, date(2026, 12, 31))
    add_completion(session, other_owner, foreign_habit, date(2026, 12, 30))
    repository = SqlAlchemyHabitCompletionReadRepository(session)

    first = repository.list_by_owner_and_habit(owner_id, habit.id, 1, 2)
    second = repository.list_by_owner_and_habit(owner_id, habit.id, 2, 2)
    beyond = repository.list_by_owner_and_habit(owner_id, habit.id, 4, 2)
    empty = repository.list_by_owner_and_habit(UserId.new(), habit.id, 1, 20)
    expected = sorted(stored, key=lambda item: (item.record_date, item.id.value), reverse=True)

    assert first.items == tuple(
        HabitCompletionDTO(item.id.value, item.habit_id.value, item.record_date)
        for item in expected[:2]
    )
    assert second.items == tuple(
        HabitCompletionDTO(item.id.value, item.habit_id.value, item.record_date)
        for item in expected[2:4]
    )
    assert (first.page, first.size, first.total_items, first.total_pages) == (1, 2, 5, 3)
    assert (second.page, second.size, second.total_items, second.total_pages) == (2, 2, 5, 3)
    assert beyond.items == ()
    assert (beyond.page, beyond.total_items, beyond.total_pages) == (4, 5, 3)
    assert empty.items == ()
    assert empty.total_items == empty.total_pages == 0
    assert set(first.items[0].__dataclass_fields__) == {"id", "habit_id", "record_date"}

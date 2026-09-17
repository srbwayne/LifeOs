from collections.abc import Iterator
from datetime import date, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.infrastructure.persistence.repositories.habit_completion_read_repository import (
    SqlAlchemyHabitCompletionReadRepository,
)
from app.habits.infrastructure.persistence.repositories.habit_completion_repository import (
    SqlAlchemyHabitCompletionRepository,
)
from app.habits.infrastructure.persistence.repositories.habit_repository import (
    SqlAlchemyHabitRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base


@pytest.fixture
def session(tmp_path) -> Iterator[Session]:
    engine = create_engine(f"sqlite:///{(tmp_path / 'habit-streak.db').resolve()}")
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
            email=f"{owner_id.value}@streak.test",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )


def add_habit(session: Session, owner_id: UserId, name: str) -> Habit:
    habit = Habit.create(owner_id, name)
    SqlAlchemyHabitRepository(session).save(habit)
    session.flush()
    return habit


def add_completion(session: Session, owner_id: UserId, habit: Habit, record_date: date) -> None:
    SqlAlchemyHabitCompletionRepository(session).save(
        HabitCompletion.create(owner_id, habit.id, record_date)
    )
    session.flush()


def test_streak_projection_is_owner_and_habit_scoped_until_date(session: Session) -> None:
    owner_id = UserId.new()
    other_owner = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner)
    target = add_habit(session, owner_id, "Target")
    other_habit = add_habit(session, owner_id, "Other")
    foreign_habit = add_habit(session, other_owner, "Foreign")
    evaluation_date = date(2026, 9, 14)
    add_completion(session, owner_id, target, evaluation_date - timedelta(days=2))
    add_completion(session, owner_id, target, evaluation_date)
    add_completion(session, owner_id, target, evaluation_date + timedelta(days=1))
    add_completion(session, owner_id, other_habit, evaluation_date)
    add_completion(session, other_owner, foreign_habit, evaluation_date)

    result = SqlAlchemyHabitCompletionReadRepository(
        session
    ).list_record_dates_by_owner_and_habit_until(owner_id, target.id, evaluation_date)

    assert result == (evaluation_date, evaluation_date - timedelta(days=2))
    assert all(isinstance(item, date) for item in result)
    assert (
        SqlAlchemyHabitCompletionReadRepository(session).list_record_dates_by_owner_and_habit_until(
            other_owner, target.id, evaluation_date
        )
        == ()
    )

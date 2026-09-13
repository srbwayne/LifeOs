from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.habits.domain.aggregates.habit import Habit
from app.habits.infrastructure.persistence.repositories.habit_read_repository import (
    SqlAlchemyHabitReadRepository,
)
from app.habits.infrastructure.persistence.repositories.habit_repository import (
    SqlAlchemyHabitRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base


@pytest.fixture
def session(tmp_path):
    engine = create_engine(f"sqlite:///{(tmp_path / 'habits-read.db').resolve()}")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, user_id: UserId) -> None:
    now = datetime.now()
    session.add(
        UserModel(
            id=user_id.value,
            email=f"{user_id.value}@example.test",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )


def add_habit(session: Session, owner_id: UserId, name: str, active: bool = True) -> None:
    habit = Habit.create(owner_id, name, "  Details  ")
    if not active:
        habit.deactivate()
    SqlAlchemyHabitRepository(session).save(habit)
    session.flush()


def test_list_by_owner_projects_all_states_with_deterministic_order(session: Session) -> None:
    owner_id = UserId.new()
    other_owner = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner)
    add_habit(session, owner_id, "B")
    add_habit(session, owner_id, "A", active=False)
    add_habit(session, other_owner, "AA")

    result = SqlAlchemyHabitReadRepository(session).list_by_owner(owner_id)

    assert [(item.name, item.active, item.description) for item in result] == [
        ("A", False, "Details"),
        ("B", True, "Details"),
    ]


def test_list_by_owner_returns_empty_tuple_without_completion_dependency(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)

    assert SqlAlchemyHabitReadRepository(session).list_by_owner(owner_id) == ()

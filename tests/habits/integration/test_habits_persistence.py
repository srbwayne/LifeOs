from datetime import date, datetime
from typing import Any, cast

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.domain.value_objects.habit_completion_id import HabitCompletionId
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.infrastructure.persistence.mappers.habit_completion_mapper import (
    HabitCompletionMapper,
)
from app.habits.infrastructure.persistence.mappers.habit_mapper import HabitMapper
from app.habits.infrastructure.persistence.models.habit_completion_model import (
    HabitCompletionModel,
)
from app.habits.infrastructure.persistence.models.habit_model import HabitModel
from app.habits.infrastructure.persistence.repositories.habit_completion_repository import (
    SqlAlchemyHabitCompletionRepository,
)
from app.habits.infrastructure.persistence.repositories.habit_repository import (
    SqlAlchemyHabitRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base


@pytest.fixture
def session(tmp_path):
    engine = create_engine(f"sqlite:///{(tmp_path / 'habits.db').resolve()}")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, user_id: UserId) -> None:
    now = datetime.now()
    session.add(
        UserModel(
            id=user_id.to_persistence(),
            email=f"{user_id.value}@example.test",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )


def persist_habit(session: Session, owner_id: UserId, name: str = "Example") -> Habit:
    habit = Habit.create(owner_id, name, "  Details  ")
    SqlAlchemyHabitRepository(session).save(habit)
    session.flush()
    return habit


def persist_completion(
    session: Session,
    owner_id: UserId,
    habit_id: HabitId,
    record_date: date = date(2026, 9, 12),
) -> HabitCompletion:
    completion = HabitCompletion.create(owner_id, habit_id, record_date)
    SqlAlchemyHabitCompletionRepository(session).save(completion)
    session.flush()
    return completion


def test_mappers_round_trip_without_technical_timestamps_in_domain(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    habit = Habit.create(owner_id, "  Example  ", "  Details  ")
    habit_model = HabitMapper.to_persistence(habit)
    session.add(habit_model)
    session.flush()

    restored_habit_model = session.get(HabitModel, habit.id.value)
    assert restored_habit_model is not None
    restored_habit = HabitMapper.to_domain(restored_habit_model)
    assert restored_habit == habit
    assert restored_habit.description == "Details"
    assert not hasattr(restored_habit, "created_at")
    assert not hasattr(restored_habit, "updated_at")

    completion = HabitCompletion.create(owner_id, habit.id, date(2026, 9, 12))
    completion_model = HabitCompletionMapper.to_persistence(completion)
    session.add(completion_model)
    session.flush()
    restored_completion_model = session.get(HabitCompletionModel, completion.id.value)
    assert restored_completion_model is not None
    restored_completion = HabitCompletionMapper.to_domain(restored_completion_model)
    assert restored_completion == completion
    assert restored_completion.record_date == date(2026, 9, 12)
    assert not hasattr(restored_completion, "created_at")


def test_habit_repository_is_owner_scoped_exact_and_updates_only_lifecycle(
    session: Session,
) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    habit = persist_habit(session, owner_a)
    repository = SqlAlchemyHabitRepository(session)

    assert repository.get_by_id_and_owner(habit.id, owner_a) == habit
    assert repository.get_by_id_and_owner(habit.id, owner_b) is None
    assert repository.get_by_owner_and_name(owner_a, "Example") == habit
    assert repository.get_by_owner_and_name(owner_a, "example") is None
    assert repository.get_by_owner_and_name(owner_b, "Example") is None

    persisted_before = session.get(HabitModel, habit.id.value)
    assert persisted_before is not None
    before = persisted_before.updated_at
    habit.deactivate()
    repository.save(habit)
    session.flush()
    persisted = session.get(HabitModel, habit.id.value)
    assert persisted is not None
    assert persisted.active is False
    assert persisted.updated_at >= before


def test_habit_repository_does_not_commit_and_rejects_immutable_conflicts(session: Session) -> None:
    owner_id = UserId.new()
    other_owner = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner)
    habit = persist_habit(session, owner_id)
    repository = SqlAlchemyHabitRepository(session)

    session.expire_all()
    assert session.get(HabitModel, habit.id.value) is not None
    for forged in (
        Habit.restore(habit.id, other_owner, habit.name, habit.description, True),
        Habit.restore(habit.id, owner_id, "Changed", habit.description, True),
        Habit.restore(habit.id, owner_id, habit.name, "Changed", True),
    ):
        with pytest.raises(ValueError, match="immutable persistence fields conflict"):
            repository.save(forged)


def test_habit_name_constraint_is_owner_scoped(session: Session) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    persist_habit(session, owner_a, "Same")
    persist_habit(session, owner_b, "Same")
    duplicate = Habit.create(owner_a, "Same")
    SqlAlchemyHabitRepository(session).save(duplicate)

    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_completion_repository_round_trip_lookup_and_delete_are_owner_scoped(
    session: Session,
) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    habit = persist_habit(session, owner_a)
    completion = persist_completion(session, owner_a, habit.id)
    repository = SqlAlchemyHabitCompletionRepository(session)

    assert (
        repository.get_by_owner_habit_date(owner_a, habit.id, completion.record_date) == completion
    )
    assert repository.get_by_owner_habit_date(owner_b, habit.id, completion.record_date) is None
    assert (
        repository.get_by_owner_habit_date(owner_a, HabitId.new(), completion.record_date) is None
    )
    assert repository.get_by_owner_habit_date(owner_a, habit.id, date(2026, 9, 13)) is None

    repository.delete(completion)
    session.flush()
    assert repository.get_by_owner_habit_date(owner_a, habit.id, completion.record_date) is None
    repository.delete(completion)


def test_completion_repository_rejects_duplicate_business_key_without_recovery(
    session: Session,
) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    habit = persist_habit(session, owner_id)
    persist_completion(session, owner_id, habit.id)
    duplicate = HabitCompletion.create(owner_id, habit.id, date(2026, 9, 12))
    SqlAlchemyHabitCompletionRepository(session).save(duplicate)

    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_completion_repository_rejects_immutable_conflict_on_same_id(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    habit = persist_habit(session, owner_id)
    completion = persist_completion(session, owner_id, habit.id)
    repository = SqlAlchemyHabitCompletionRepository(session)
    forged = HabitCompletion.restore(
        completion.id,
        owner_id,
        habit.id,
        date(2026, 9, 13),
    )

    with pytest.raises(ValueError, match="immutable persistence fields conflict"):
        repository.save(forged)


def test_completion_owner_safe_foreign_key_and_missing_habit_are_restricted(
    session: Session,
) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    habit = persist_habit(session, owner_a)

    session.add(
        HabitCompletionModel(
            id=HabitCompletionId.new().value,
            user_id=owner_b.value,
            habit_id=habit.id.value,
            record_date=date(2026, 9, 12),
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()

    session.add(
        HabitCompletionModel(
            id=HabitCompletionId.new().value,
            user_id=owner_a.value,
            habit_id=HabitId.new().value,
            record_date=date(2026, 9, 12),
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_habit_and_owner_delete_are_restricted_when_completion_exists(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    habit = persist_habit(session, owner_id)
    persist_completion(session, owner_id, habit.id)
    session.commit()

    session.delete(session.get(HabitModel, habit.id.value))
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()

    owner = session.get(UserModel, owner_id.value)
    assert owner is not None
    session.delete(owner)
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_persistence_models_match_required_columns_and_no_active_index() -> None:
    assert list(HabitModel.__table__.columns.keys()) == [
        "id",
        "user_id",
        "name",
        "description",
        "active",
        "created_at",
        "updated_at",
    ]
    assert list(HabitCompletionModel.__table__.columns.keys()) == [
        "id",
        "user_id",
        "habit_id",
        "record_date",
        "created_at",
    ]
    assert str(HabitModel.__table__.c.name.type) == "TEXT"
    assert str(HabitCompletionModel.__table__.c.record_date.type) == "DATE"
    habit_table = cast(Any, HabitModel.__table__)
    assert not any("active" in index.name for index in habit_table.indexes)


def test_technical_created_at_is_persisted(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    habit = persist_habit(session, owner_id)
    completion = persist_completion(session, owner_id, habit.id)

    habit_model = session.get(HabitModel, habit.id.value)
    completion_model = session.get(HabitCompletionModel, completion.id.value)
    assert habit_model is not None and habit_model.created_at is not None
    assert habit_model.updated_at is not None
    assert completion_model is not None and completion_model.created_at is not None

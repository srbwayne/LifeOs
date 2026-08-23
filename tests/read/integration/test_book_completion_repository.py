from collections.abc import Iterator
from datetime import datetime, timezone
from typing import cast

import pytest
from sqlalchemy import Table, UniqueConstraint, create_engine, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.value_objects.book_id import BookId
from app.read.infrastructure.persistence.models.book_completion_model import (
    BookCompletionModel,
)
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.repositories.book_completion_repository import (
    SqlAlchemyBookCompletionRepository,
)
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base

COMPLETED_AT = datetime(2026, 8, 22, 21, 0, tzinfo=timezone.utc)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    with session_factory() as database_session:
        yield database_session
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, user_id: UserId) -> None:
    now = datetime(2026, 8, 22)
    session.add(
        UserModel(
            id=user_id.to_persistence(),
            email=f"{user_id.to_persistence()}@example.com",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )
    session.commit()


def add_book(session: Session, owner_id: UserId) -> Book:
    book = Book.create(owner_id, "Book", "Author", 300)
    SqlAlchemyBookRepository(session).save(book)
    session.commit()
    return book


def make_completion(book_id: BookId) -> BookCompletion:
    return BookCompletion.create(book_id, COMPLETED_AT)


def test_sqlite_foreign_key_policy_is_enabled(session: Session) -> None:
    assert session.scalar(text("PRAGMA foreign_keys")) == 1


def test_save_adds_completion_without_committing_and_rollback_discards_it(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    completion = make_completion(book.id)

    SqlAlchemyBookCompletionRepository(session).save(completion)

    assert any(
        isinstance(model, BookCompletionModel) and model.id == completion.id.to_persistence()
        for model in session.new
    )
    session.rollback()
    assert session.get(BookCompletionModel, completion.id.to_persistence()) is None


def test_repository_persists_and_restores_completion_for_its_owner(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    completion = make_completion(book.id)
    repository = SqlAlchemyBookCompletionRepository(session)

    repository.save(completion)
    session.commit()

    model = session.get(BookCompletionModel, completion.id.to_persistence())
    restored = repository.get_by_book_and_owner(book.id, owner_id)
    assert model is not None
    assert model.book_id == book.id.to_persistence()
    assert model.completed_at == COMPLETED_AT.replace(tzinfo=None)
    assert model.created_at is not None
    assert restored is not None
    assert restored.id == completion.id
    assert restored.book_id == book.id
    assert restored.completed_at == COMPLETED_AT
    assert restored.completed_at.tzinfo is timezone.utc
    assert restored.domain_events == []


def test_owner_safe_lookup_returns_none_for_other_owner(session: Session) -> None:
    owner_id = UserId.new()
    other_owner_id = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner_id)
    book = add_book(session, owner_id)
    completion = make_completion(book.id)
    repository = SqlAlchemyBookCompletionRepository(session)
    repository.save(completion)
    session.commit()

    assert repository.get_by_book_and_owner(book.id, owner_id) == completion
    assert repository.get_by_book_and_owner(book.id, other_owner_id) is None
    assert repository.get_by_book_and_owner(BookId.new(), owner_id) is None


def test_duplicate_completion_for_book_is_rejected_without_upsert(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    repository = SqlAlchemyBookCompletionRepository(session)
    original = make_completion(book.id)
    repository.save(original)
    session.commit()

    repository.save(make_completion(book.id))
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()

    model = session.get(BookCompletionModel, original.id.to_persistence())
    assert model is not None
    assert model.id == original.id.to_persistence()


def test_foreign_keys_reject_missing_book_and_accept_valid_book(session: Session) -> None:
    repository = SqlAlchemyBookCompletionRepository(session)
    repository.save(make_completion(BookId.new()))

    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()

    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    repository.save(make_completion(book.id))
    session.commit()

    assert session.execute(text("PRAGMA foreign_key_check")).all() == []


def test_restrict_prevents_deleting_referenced_book(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    completion = make_completion(book.id)
    SqlAlchemyBookCompletionRepository(session).save(completion)
    session.commit()

    model = session.get(BookModel, book.id.to_persistence())
    assert model is not None
    session.delete(model)
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()

    assert session.get(BookModel, book.id.to_persistence()) is not None
    assert session.get(BookCompletionModel, completion.id.to_persistence()) is not None


def test_model_metadata_has_one_unique_book_id_and_required_composite_index(
    session: Session,
) -> None:
    table = cast(Table, BookCompletionModel.__table__)
    unique_book_id_constraints = [
        constraint
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
        and tuple(column.name for column in constraint.columns) == ("book_id",)
    ]
    assert len(unique_book_id_constraints) == 1
    assert {
        (index.name, tuple(column.name for column in index.columns)) for index in table.indexes
    } == {("ix_book_completions_completed_at_book_id", ("completed_at", "book_id"))}
    assert session.bind is not None
    database_indexes = inspect(session.bind).get_indexes("book_completions")
    assert {(index["name"], tuple(index["column_names"])) for index in database_indexes} == {
        ("ix_book_completions_completed_at_book_id", ("completed_at", "book_id"))
    }


def test_completion_model_contains_no_ownership_or_update_columns() -> None:
    columns = BookCompletionModel.__table__.c
    assert columns.get("owner_id") is None
    assert columns.get("user_id") is None
    assert columns.get("updated_at") is None

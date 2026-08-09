from collections.abc import Iterator
from datetime import datetime

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.application.commands.create_book import (
    CreateBookCommand,
    CreateBookCommandHandler,
)
from app.read.domain.aggregates.book import Book
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.shared.application.event_bus import InMemoryEventBus
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


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
    now = datetime(2026, 8, 9, 0, 0, 0)
    session.add(
        UserModel(
            id=user_id.to_persistence(),
            email=f"{user_id}@example.com",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )
    session.commit()


def book_count(session: Session) -> int:
    return session.scalar(select(func.count()).select_from(BookModel)) or 0


def test_command_commit_persists_book_with_shared_session(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    repository = SqlAlchemyBookRepository(session)
    unit_of_work = SqlAlchemyUnitOfWork(session, InMemoryEventBus())
    handler = CreateBookCommandHandler(repository, unit_of_work)

    result = handler(CreateBookCommand(owner_id, "Book", "Author", 100))

    assert repository._session is unit_of_work.session
    assert session.get(BookModel, result.id) is not None
    assert book_count(session) == 1


def test_context_without_commit_does_not_persist_after_session_rollback(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    repository = SqlAlchemyBookRepository(session)
    unit_of_work = SqlAlchemyUnitOfWork(session, InMemoryEventBus())

    with unit_of_work:
        repository.save(Book.create(owner_id, "Book", "Author", 100))
    unit_of_work.rollback()

    assert book_count(session) == 0


def test_exception_rolls_back_pending_book(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    repository = SqlAlchemyBookRepository(session)
    unit_of_work = SqlAlchemyUnitOfWork(session, InMemoryEventBus())

    with pytest.raises(RuntimeError, match="failure"), unit_of_work:
        repository.save(Book.create(owner_id, "Book", "Author", 100))
        session.flush()
        raise RuntimeError("failure")

    assert book_count(session) == 0

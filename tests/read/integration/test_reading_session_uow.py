from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.application.commands.create_reading_session import (
    CreateReadingSessionCommand,
    CreateReadingSessionCommandHandler,
)
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.errors.reading_session_errors import ReadingBeyondBookError
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.read.infrastructure.persistence.repositories.reading_session_repository import (
    SqlAlchemyReadingSessionRepository,
)
from app.shared.application.event_bus import InMemoryEventBus
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

START = datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc)
END = datetime(2026, 8, 9, 12, 30, tzinfo=timezone.utc)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    with session_factory() as database_session:
        yield database_session
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, user_id: UserId) -> None:
    now = datetime(2026, 8, 9)
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


def add_book(session: Session, owner_id: UserId) -> Book:
    book = Book.create(owner_id, "Book", "Author", 100)
    SqlAlchemyBookRepository(session).save(book)
    session.commit()
    return book


def session_count(session: Session) -> int:
    return session.scalar(select(func.count()).select_from(ReadingSessionModel)) or 0


def build_handler(
    session: Session,
) -> tuple[
    CreateReadingSessionCommandHandler,
    SqlAlchemyBookRepository,
    SqlAlchemyReadingSessionRepository,
    SqlAlchemyUnitOfWork,
]:
    book_repository = SqlAlchemyBookRepository(session)
    reading_session_repository = SqlAlchemyReadingSessionRepository(session)
    unit_of_work = SqlAlchemyUnitOfWork(session, InMemoryEventBus())
    return (
        CreateReadingSessionCommandHandler(
            book_repository,
            reading_session_repository,
            unit_of_work,
        ),
        book_repository,
        reading_session_repository,
        unit_of_work,
    )


def command(owner_id: UserId, book: Book, *, end_page: int = 12) -> CreateReadingSessionCommand:
    return CreateReadingSessionCommand(
        owner_id=owner_id,
        book_id=book.id,
        start_page=10,
        end_page=end_page,
        started_at=START,
        ended_at=END,
        notes="reflection",
    )


def test_handler_uses_shared_session_and_commit_persists(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    handler, book_repository, reading_repository, unit_of_work = build_handler(session)

    result = handler(command(owner_id, book))

    assert book_repository._session is unit_of_work.session
    assert reading_repository._session is unit_of_work.session
    assert session_count(session) == 1
    assert session.get(ReadingSessionModel, result.id) is not None
    assert result.pages_read == 3


def test_missing_book_does_not_persist(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    missing_book = Book.create(owner_id, "Missing", "Author", 100)
    handler, _, _, _ = build_handler(session)

    with pytest.raises(BookNotFoundError):
        handler(command(owner_id, missing_book))

    assert session_count(session) == 0


def test_other_owner_book_does_not_persist(session: Session) -> None:
    owner_id = UserId.new()
    other_owner = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner)
    hidden_book = add_book(session, other_owner)
    handler, _, _, _ = build_handler(session)

    with pytest.raises(BookNotFoundError):
        handler(command(owner_id, hidden_book))

    assert session_count(session) == 0


def test_domain_error_does_not_persist(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    handler, _, _, _ = build_handler(session)

    with pytest.raises(ReadingBeyondBookError):
        handler(command(owner_id, book, end_page=101))

    assert session_count(session) == 0


def test_exception_rolls_back_pending_session(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    repository = SqlAlchemyReadingSessionRepository(session)
    unit_of_work = SqlAlchemyUnitOfWork(session, InMemoryEventBus())
    reading_session = ReadingSession.create(
        owner_id=owner_id,
        book_id=book.id,
        start_page=1,
        end_page=1,
        started_at=START,
        ended_at=END,
        book_total_pages=book.total_pages,
    )

    with pytest.raises(RuntimeError, match="failure"), unit_of_work:
        repository.save(reading_session)
        session.flush()
        raise RuntimeError("failure")

    assert session_count(session) == 0

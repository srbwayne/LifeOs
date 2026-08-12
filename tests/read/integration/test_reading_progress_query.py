from collections.abc import Iterator
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.application.queries.get_reading_progress import (
    GetReadingProgressQuery,
    GetReadingProgressQueryHandler,
)
from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.read.infrastructure.persistence.repositories.reading_session_repository import (
    SqlAlchemyReadingSessionRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base

NOW = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)


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
    session.add(
        UserModel(
            id=user_id.to_persistence(),
            email=f"{user_id}@example.com",
            hashed_password="hash",
            created_at=NOW.replace(tzinfo=None),
            updated_at=NOW.replace(tzinfo=None),
        )
    )
    session.commit()


def add_book(session: Session, owner_id: UserId, pages: int = 100) -> Book:
    book = Book.create(owner_id, "Book", "Author", pages)
    SqlAlchemyBookRepository(session).save(book)
    session.commit()
    return book


def add_reading_session(
    session: Session,
    owner_id: UserId,
    book: Book,
    start_page: int,
    end_page: int,
) -> None:
    repository = SqlAlchemyReadingSessionRepository(session)
    repository.save(
        ReadingSession.create(
            owner_id=owner_id,
            book_id=book.id,
            start_page=start_page,
            end_page=end_page,
            started_at=NOW,
            ended_at=NOW,
            book_total_pages=book.total_pages,
        )
    )
    session.commit()


def build_handler(session: Session) -> GetReadingProgressQueryHandler:
    return GetReadingProgressQueryHandler(
        SqlAlchemyBookRepository(session),
        SqlAlchemyReadingSessionRepository(session),
        ReadingProgressCalculator(),
    )


def test_real_query_returns_zero_and_overlapping_progress(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    empty_book = add_book(session, owner_id)
    covered_book = add_book(session, owner_id)
    handler = build_handler(session)

    empty = handler(GetReadingProgressQuery(owner_id, empty_book.id))
    add_reading_session(session, owner_id, covered_book, 1, 20)
    add_reading_session(session, owner_id, covered_book, 15, 30)
    covered = handler(GetReadingProgressQuery(owner_id, covered_book.id))

    assert empty.unique_pages_read == 0
    assert empty.percentage == Decimal("0.00")
    assert covered.unique_pages_read == 30
    assert covered.highest_page_reached == 30
    assert covered.percentage == Decimal("30.00")


@pytest.mark.parametrize("existing_for_other_owner", [False, True])
def test_real_query_hides_missing_and_other_owner_books(
    session: Session,
    existing_for_other_owner: bool,
) -> None:
    owner_id = UserId.new()
    other_owner_id = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner_id)
    requested_book = (
        add_book(session, other_owner_id)
        if existing_for_other_owner
        else Book.create(owner_id, "Missing", "Author", 100)
    )
    handler = build_handler(session)

    with pytest.raises(BookNotFoundError, match="Book not found"):
        handler(GetReadingProgressQuery(owner_id, requested_book.id))

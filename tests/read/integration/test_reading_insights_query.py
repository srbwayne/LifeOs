from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.application.queries.get_reading_insights import (
    GetReadingInsightsQuery,
    GetReadingInsightsQueryHandler,
)
from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.read.domain.services.reading_insights_calculator import ReadingInsightsCalculator
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.read.infrastructure.persistence.repositories.reading_session_repository import (
    SqlAlchemyReadingSessionRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base

NOW = datetime(2026, 8, 14, tzinfo=timezone.utc)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine)() as database_session:
        yield database_session
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, user: UserId) -> None:
    session.add(
        UserModel(
            id=user.to_persistence(),
            email=f"{user}@example.com",
            hashed_password="hash",
            created_at=NOW.replace(tzinfo=None),
            updated_at=NOW.replace(tzinfo=None),
        )
    )
    session.commit()


def add_book(session: Session, owner: UserId) -> Book:
    book = Book.create(owner, "Book", "Author", 100)
    SqlAlchemyBookRepository(session).save(book)
    session.commit()
    return book


def add_session(session: Session, book: Book, start: int, end: int) -> None:
    SqlAlchemyReadingSessionRepository(session).save(
        ReadingSession.create(book.owner_id, book.id, start, end, NOW, NOW, book.total_pages)
    )
    session.commit()


def handler(session: Session) -> GetReadingInsightsQueryHandler:
    return GetReadingInsightsQueryHandler(
        SqlAlchemyBookRepository(session),
        SqlAlchemyReadingSessionRepository(session),
        ReadingCoverageCalculator(),
        ReadingProgressCalculator(),
        ReadingInsightsCalculator(),
    )


def test_real_repositories_return_empty_and_gapped_insights(session: Session) -> None:
    owner = UserId.new()
    add_user(session, owner)
    empty = add_book(session, owner)
    covered = add_book(session, owner)
    assert handler(session)(GetReadingInsightsQuery(owner, empty.id)).remaining_pages == 100
    add_session(session, covered, 1, 30)
    add_session(session, covered, 50, 60)
    result = handler(session)(GetReadingInsightsQuery(owner, covered.id))
    assert [(gap.start_page, gap.end_page) for gap in result.gaps] == [(31, 49), (61, 100)]
    assert result.remaining_pages == 59
    assert not session.new and not session.dirty


@pytest.mark.parametrize("foreign", [False, True])
def test_real_repositories_hide_missing_and_foreign_books(session: Session, foreign: bool) -> None:
    owner = UserId.new()
    other = UserId.new()
    add_user(session, owner)
    add_user(session, other)
    requested = (
        add_book(session, other).id if foreign else Book.create(owner, "Missing", "Author", 100).id
    )
    with pytest.raises(BookNotFoundError, match="Book not found"):
        handler(session)(GetReadingInsightsQuery(owner, requested))

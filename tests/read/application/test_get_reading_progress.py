from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.read.application.dtos.reading_progress_dto import ReadingProgressDTO
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.application.queries.get_reading_progress import (
    GetReadingProgressQuery,
    GetReadingProgressQueryHandler,
)
from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.models.reading_progress import ReadingProgress
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId

NOW = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)


class FakeBookRepository:
    def __init__(self, books: tuple[Book, ...] = ()) -> None:
        self.books = books
        self.lookups: list[tuple[BookId, UserId]] = []
        self.save_count = 0
        self.list_count = 0

    def save(self, book: Book) -> None:
        self.save_count += 1

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]:
        self.list_count += 1
        raise AssertionError("Reading progress must not list the library.")

    def get_by_id_and_owner(self, book_id: BookId, owner_id: UserId) -> Book | None:
        self.lookups.append((book_id, owner_id))
        return next(
            (book for book in self.books if book.id == book_id and book.owner_id == owner_id),
            None,
        )


class FakeReadingSessionRepository:
    def __init__(self, sessions: tuple[ReadingSession, ...] = ()) -> None:
        self.sessions = sessions
        self.lookups: list[tuple[BookId, UserId]] = []
        self.save_count = 0

    def save(self, session: ReadingSession) -> None:
        self.save_count += 1

    def list_by_book_and_owner(
        self,
        book_id: BookId,
        owner_id: UserId,
    ) -> tuple[ReadingSession, ...]:
        self.lookups.append((book_id, owner_id))
        return tuple(
            session
            for session in self.sessions
            if session.book_id == book_id and session.owner_id == owner_id
        )


def make_session(
    owner_id: UserId,
    book: Book,
    start_page: int,
    end_page: int,
) -> ReadingSession:
    return ReadingSession.create(
        owner_id=owner_id,
        book_id=book.id,
        start_page=start_page,
        end_page=end_page,
        started_at=NOW,
        ended_at=NOW,
        book_total_pages=book.total_pages,
    )


def build_handler(
    books: tuple[Book, ...],
    sessions: tuple[ReadingSession, ...] = (),
    calculator: ReadingProgressCalculator | None = None,
) -> tuple[
    GetReadingProgressQueryHandler,
    FakeBookRepository,
    FakeReadingSessionRepository,
]:
    book_repository = FakeBookRepository(books)
    session_repository = FakeReadingSessionRepository(sessions)
    handler = GetReadingProgressQueryHandler(
        book_repository,
        session_repository,
        calculator or ReadingProgressCalculator(),
    )
    return handler, book_repository, session_repository


def test_query_is_immutable_and_preserves_owner_and_book() -> None:
    owner_id = UserId.new()
    book_id = BookId.new()
    query = GetReadingProgressQuery(owner_id=owner_id, book_id=book_id)

    assert query.owner_id == owner_id
    assert query.book_id == book_id
    with pytest.raises(FrozenInstanceError):
        query.book_id = BookId.new()  # type: ignore[misc]


def test_handler_uses_owner_scoped_repositories_and_calculator() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 100)
    sessions = (make_session(owner_id, book, 1, 20),)
    expected_progress = ReadingProgress(
        book_id=book.id,
        total_pages=100,
        unique_pages_read=20,
        highest_page_reached=20,
        percentage=Decimal("20.00"),
        completed=False,
    )
    calculator = Mock(spec=ReadingProgressCalculator)
    calculator.calculate.return_value = expected_progress
    handler, book_repository, session_repository = build_handler((book,), sessions, calculator)

    result = handler(GetReadingProgressQuery(owner_id, book.id))

    assert book_repository.lookups == [(book.id, owner_id)]
    assert session_repository.lookups == [(book.id, owner_id)]
    calculator.calculate.assert_called_once_with(book, sessions)
    assert result == ReadingProgressDTO.from_progress(expected_progress)
    assert book_repository.save_count == 0
    assert session_repository.save_count == 0


def test_book_without_sessions_returns_zero_progress() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 100)
    handler, _, session_repository = build_handler((book,))

    result = handler(GetReadingProgressQuery(owner_id, book.id))

    assert session_repository.lookups == [(book.id, owner_id)]
    assert result == ReadingProgressDTO(
        book_id=book.id.to_persistence(),
        total_pages=100,
        unique_pages_read=0,
        highest_page_reached=None,
        percentage=Decimal("0.00"),
        completed=False,
    )


@pytest.mark.parametrize("other_owner", [False, True])
def test_missing_or_other_owner_book_is_indistinguishable(other_owner: bool) -> None:
    owner_id = UserId.new()
    book_id = BookId.new()
    books: tuple[Book, ...] = ()
    if other_owner:
        hidden = Book.create(UserId.new(), "Hidden", "Author", 100)
        books = (
            Book.restore(
                id=book_id,
                owner_id=hidden.owner_id,
                title=hidden.title,
                author=hidden.author,
                total_pages=hidden.total_pages,
            ),
        )
    calculator = Mock(spec=ReadingProgressCalculator)
    handler, book_repository, session_repository = build_handler(books, calculator=calculator)

    with pytest.raises(BookNotFoundError, match="Book not found"):
        handler(GetReadingProgressQuery(owner_id, book_id))

    assert book_repository.lookups == [(book_id, owner_id)]
    assert session_repository.lookups == []
    assert book_repository.save_count == 0
    assert session_repository.save_count == 0
    calculator.calculate.assert_not_called()


def test_dto_preserves_decimal_omits_owner_and_is_immutable() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 3)
    session = make_session(owner_id, book, 1, 2)
    handler, _, _ = build_handler((book,), (session,))

    result = handler(GetReadingProgressQuery(owner_id, book.id))

    assert result.book_id == book.id.to_persistence()
    assert result.total_pages == 3
    assert result.unique_pages_read == 2
    assert result.highest_page_reached == 2
    assert result.percentage == Decimal("66.67")
    assert isinstance(result.percentage, Decimal)
    assert result.completed is False
    assert not hasattr(result, "owner_id")
    assert not hasattr(result, "user_id")
    with pytest.raises(FrozenInstanceError):
        result.completed = True  # type: ignore[misc]

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from app.read.application.dtos.reading_insights_dto import PageIntervalDTO, ReadingInsightsDTO
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.application.queries.get_reading_insights import (
    GetReadingInsightsQuery,
    GetReadingInsightsQueryHandler,
)
from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.models.page_interval import PageInterval
from app.read.domain.models.reading_coverage import ReadingCoverage
from app.read.domain.models.reading_insights import ReadingInsights
from app.read.domain.models.reading_progress import ReadingProgress
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.read.domain.services.reading_insights_calculator import ReadingInsightsCalculator
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId

NOW = datetime(2026, 8, 14, tzinfo=timezone.utc)


def make_session(book: Book, start: int, end: int) -> ReadingSession:
    return ReadingSession.create(book.owner_id, book.id, start, end, NOW, NOW, book.total_pages)


def build_handler(book: Book | None, sessions: tuple[ReadingSession, ...] = ()):
    books = Mock()
    books.get_by_id_and_owner.return_value = book
    sessions_repo = Mock()
    sessions_repo.list_by_book_and_owner.return_value = sessions
    coverage = Mock(spec=ReadingCoverageCalculator)
    progress = Mock(spec=ReadingProgressCalculator)
    insights = Mock(spec=ReadingInsightsCalculator)
    handler = GetReadingInsightsQueryHandler(books, sessions_repo, coverage, progress, insights)
    return handler, books, sessions_repo, coverage, progress, insights


def test_query_is_frozen() -> None:
    query = GetReadingInsightsQuery(UserId.new(), BookId.new())
    with pytest.raises(FrozenInstanceError):
        query.book_id = BookId.new()  # type: ignore[misc]


def test_handler_calls_owner_scoped_repositories_and_calculators_in_order() -> None:
    owner = UserId.new()
    book = Book.create(owner, "Book", "Author", 100)
    sessions = (make_session(book, 1, 30),)
    coverage_result = ReadingCoverage((PageInterval(1, 30),))
    progress_result = ReadingProgress(
        book.id, 100, 30, 30, __import__("decimal").Decimal("30.00"), False
    )
    insights_result = ReadingInsights(book.id, 70, (PageInterval(31, 100),), False, False)
    handler, books, session_repo, coverage, progress, insights = build_handler(book, sessions)
    calls: list[str] = []

    def calculate_coverage(value: tuple[ReadingSession, ...]) -> ReadingCoverage:
        calls.append("coverage")
        return coverage_result

    def calculate_progress(value: Book, cov: ReadingCoverage) -> ReadingProgress:
        calls.append("progress")
        return progress_result

    def calculate_insights(value: ReadingProgress, cov: ReadingCoverage) -> ReadingInsights:
        calls.append("insights")
        return insights_result

    coverage.calculate.side_effect = calculate_coverage
    progress.calculate_from_coverage.side_effect = calculate_progress
    insights.calculate.side_effect = calculate_insights

    result = handler(GetReadingInsightsQuery(owner, book.id))

    books.get_by_id_and_owner.assert_called_once_with(book.id, owner)
    session_repo.list_by_book_and_owner.assert_called_once_with(book.id, owner)
    coverage.calculate.assert_called_once_with(sessions)
    progress.calculate_from_coverage.assert_called_once_with(book, coverage_result)
    insights.calculate.assert_called_once_with(progress_result, coverage_result)
    assert calls == ["coverage", "progress", "insights"]
    assert result == ReadingInsightsDTO(
        book.id.to_persistence(), 70, (PageIntervalDTO(31, 100),), False, False
    )
    assert not hasattr(result, "owner_id")
    assert not hasattr(result, "user_id")
    assert not books.save.called
    assert not session_repo.save.called


def test_book_without_sessions_returns_full_gap() -> None:
    owner = UserId.new()
    book = Book.create(owner, "Book", "Author", 100)
    handler = GetReadingInsightsQueryHandler(
        Mock(get_by_id_and_owner=Mock(return_value=book)),
        Mock(list_by_book_and_owner=Mock(return_value=())),
        ReadingCoverageCalculator(),
        ReadingProgressCalculator(),
        ReadingInsightsCalculator(),
    )
    result = handler(GetReadingInsightsQuery(owner, book.id))
    assert result == ReadingInsightsDTO(
        book.id.to_persistence(), 100, (PageIntervalDTO(1, 100),), False, False
    )


@pytest.mark.parametrize("foreign", [False, True])
def test_missing_and_foreign_books_are_indistinguishable(foreign: bool) -> None:
    owner = UserId.new()
    requested = BookId.new()
    hidden = Book.create(UserId.new(), "Hidden", "Author", 100) if foreign else None
    handler, books, sessions, coverage, progress, insights = build_handler(
        hidden if hidden and hidden.owner_id == owner else None
    )
    with pytest.raises(BookNotFoundError, match="Book not found"):
        handler(GetReadingInsightsQuery(owner, requested))
    books.get_by_id_and_owner.assert_called_once_with(requested, owner)
    sessions.list_by_book_and_owner.assert_not_called()
    coverage.calculate.assert_not_called()
    progress.calculate_from_coverage.assert_not_called()
    insights.calculate.assert_not_called()

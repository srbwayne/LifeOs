from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.services.reading_progress_calculator import (
    ReadingProgressCalculator,
)
from app.shared.domain.identifiers.user_id import UserId

NOW = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)


def make_book(total_pages: int = 100) -> Book:
    return Book.create(UserId.new(), "Book", "Author", total_pages)


def make_session(
    book: Book,
    start_page: int,
    end_page: int,
    *,
    started_at: datetime = NOW,
) -> ReadingSession:
    return ReadingSession.create(
        owner_id=book.owner_id,
        book_id=book.id,
        start_page=start_page,
        end_page=end_page,
        started_at=started_at,
        ended_at=started_at + timedelta(minutes=30),
        book_total_pages=book.total_pages,
    )


def calculate(
    book: Book,
    *ranges: tuple[int, int],
) -> object:
    sessions = tuple(make_session(book, start, end) for start, end in ranges)
    return ReadingProgressCalculator.calculate(book, sessions)


def test_zero_sessions_returns_zero_progress() -> None:
    book = make_book()

    progress = ReadingProgressCalculator.calculate(book, ())

    assert progress.book_id == book.id
    assert progress.total_pages == 100
    assert progress.unique_pages_read == 0
    assert progress.highest_page_reached is None
    assert progress.percentage == Decimal("0.00")
    assert progress.completed is False


@pytest.mark.parametrize(
    ("ranges", "expected"),
    [
        (((1, 1),), 1),
        (((1, 20),), 20),
        (((1, 10), (5, 15)), 15),
        (((1, 10), (1, 10)), 10),
        (((1, 10), (11, 20)), 20),
    ],
)
def test_calculates_unique_inclusive_coverage(
    ranges: tuple[tuple[int, int], ...],
    expected: int,
) -> None:
    book = make_book()

    progress = calculate(book, *ranges)

    assert progress.unique_pages_read == expected  # type: ignore[attr-defined]


def test_merges_overlapping_and_non_contiguous_intervals() -> None:
    book = make_book()

    progress = calculate(book, (1, 20), (15, 30), (50, 60))

    assert progress.unique_pages_read == 41  # type: ignore[attr-defined]
    assert progress.highest_page_reached == 60  # type: ignore[attr-defined]
    assert progress.percentage == Decimal("41.00")  # type: ignore[attr-defined]
    assert progress.completed is False  # type: ignore[attr-defined]


def test_input_order_and_session_time_do_not_change_progress() -> None:
    book = make_book()
    early = make_session(book, 50, 60, started_at=NOW)
    late = make_session(book, 1, 30, started_at=NOW + timedelta(days=1))

    forward = ReadingProgressCalculator.calculate(book, (early, late))
    reverse = ReadingProgressCalculator.calculate(book, (late, early))

    assert forward == reverse


def test_highest_page_is_historical_maximum_not_current_position() -> None:
    book = make_book()

    progress = calculate(book, (80, 90), (10, 20))

    assert progress.highest_page_reached == 90  # type: ignore[attr-defined]
    assert not hasattr(progress, "current_page")
    assert not hasattr(progress, "current_position")
    assert not hasattr(progress, "next_page")


def test_reaching_last_page_alone_does_not_complete_book() -> None:
    book = make_book()

    progress = calculate(book, (90, 100))

    assert progress.unique_pages_read == 11  # type: ignore[attr-defined]
    assert progress.highest_page_reached == 100  # type: ignore[attr-defined]
    assert progress.percentage == Decimal("11.00")  # type: ignore[attr-defined]
    assert progress.completed is False  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "ranges",
    [
        ((1, 100),),
        ((1, 20), (21, 50), (51, 100)),
        ((1, 40), (30, 70), (60, 100)),
    ],
)
def test_complete_coverage_marks_book_completed(
    ranges: tuple[tuple[int, int], ...],
) -> None:
    book = make_book()

    progress = calculate(book, *ranges)

    assert progress.unique_pages_read == 100  # type: ignore[attr-defined]
    assert progress.percentage == Decimal("100.00")  # type: ignore[attr-defined]
    assert progress.completed is True  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    ("ranges", "expected"),
    [
        (((1, 1),), Decimal("33.33")),
        (((1, 2),), Decimal("66.67")),
        (((1, 3),), Decimal("100.00")),
    ],
)
def test_percentage_uses_decimal_and_half_up_rounding(
    ranges: tuple[tuple[int, int], ...],
    expected: Decimal,
) -> None:
    book = make_book(total_pages=3)

    progress = calculate(book, *ranges)

    assert isinstance(progress.percentage, Decimal)  # type: ignore[attr-defined]
    assert progress.percentage == expected  # type: ignore[attr-defined]


def test_calculation_does_not_create_domain_events() -> None:
    book = make_book()
    session = make_session(book, 1, 10)

    progress = ReadingProgressCalculator.calculate(book, (session,))

    assert progress.book_id == book.id
    assert not hasattr(progress, "domain_events")
    assert book.domain_events == []
    assert session.domain_events == []

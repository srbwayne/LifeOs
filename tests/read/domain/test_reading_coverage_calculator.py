from datetime import datetime, timezone

import pytest

from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.models.page_interval import PageInterval
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.shared.domain.identifiers.user_id import UserId

NOW = datetime(2026, 8, 14, tzinfo=timezone.utc)


def make_sessions(*ranges: tuple[int, int], total_pages: int = 100) -> tuple[ReadingSession, ...]:
    book = Book.create(UserId.new(), "Book", "Author", total_pages)
    return tuple(
        ReadingSession.create(book.owner_id, book.id, start, end, NOW, NOW, book.total_pages)
        for start, end in ranges
    )


@pytest.mark.parametrize(
    ("ranges", "expected"),
    [
        ((), ()),
        (((1, 10),), (PageInterval(1, 10),)),
        (((1, 10), (20, 30)), (PageInterval(1, 10), PageInterval(20, 30))),
        (((1, 10), (5, 15)), (PageInterval(1, 15),)),
        (((1, 10), (11, 20)), (PageInterval(1, 20),)),
        (((1, 10), (1, 10)), (PageInterval(1, 10),)),
        (((1, 10), (1, 10), (5, 15)), (PageInterval(1, 15),)),
        (((7, 7),), (PageInterval(7, 7),)),
    ],
)
def test_normalizes_interval_coverage(
    ranges: tuple[tuple[int, int], ...], expected: tuple[PageInterval, ...]
) -> None:
    assert ReadingCoverageCalculator.calculate(make_sessions(*ranges)).covered_intervals == expected


def test_order_is_irrelevant() -> None:
    sessions = make_sessions((50, 60), (1, 20), (15, 30))
    assert ReadingCoverageCalculator.calculate(sessions) == ReadingCoverageCalculator.calculate(
        tuple(reversed(sessions))
    )


def test_large_book_uses_only_session_intervals() -> None:
    coverage = ReadingCoverageCalculator.calculate(
        make_sessions((1, 10), (999_999_990, 1_000_000_000), total_pages=1_000_000_000)
    )
    assert coverage.covered_intervals == (
        PageInterval(1, 10),
        PageInterval(999_999_990, 1_000_000_000),
    )

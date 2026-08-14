from decimal import Decimal

import pytest

from app.read.domain.models.page_interval import PageInterval
from app.read.domain.models.reading_coverage import ReadingCoverage
from app.read.domain.models.reading_progress import ReadingProgress
from app.read.domain.services.reading_insights_calculator import ReadingInsightsCalculator
from app.read.domain.value_objects.book_id import BookId


def calculate(total: int, intervals: tuple[PageInterval, ...], *, completed: bool = False):
    coverage = ReadingCoverage(intervals)
    progress = ReadingProgress(
        BookId.new(),
        total,
        coverage.unique_pages_read,
        coverage.highest_page_reached,
        Decimal("100.00") if completed else Decimal("0.00"),
        completed,
    )
    return ReadingInsightsCalculator.calculate(progress, coverage)


def test_empty_coverage() -> None:
    result = calculate(100, ())
    assert result.remaining_pages == 100
    assert result.gaps == (PageInterval(1, 100),)
    assert result.last_page_reached_with_gaps is False
    assert result.full_coverage_confirmed is False


@pytest.mark.parametrize(
    ("intervals", "gaps", "remaining"),
    [
        ((PageInterval(1, 30),), (PageInterval(31, 100),), 70),
        (
            (PageInterval(1, 30), PageInterval(50, 60)),
            (PageInterval(31, 49), PageInterval(61, 100)),
            59,
        ),
        ((PageInterval(10, 100),), (PageInterval(1, 9),), 9),
        ((PageInterval(1, 90),), (PageInterval(91, 100),), 10),
    ],
)
def test_partial_coverage(
    intervals: tuple[PageInterval, ...], gaps: tuple[PageInterval, ...], remaining: int
) -> None:
    result = calculate(100, intervals)
    assert result.gaps == gaps
    assert result.remaining_pages == remaining


def test_last_page_reached_with_gaps() -> None:
    result = calculate(100, (PageInterval(1, 50), PageInterval(100, 100)))
    assert result.gaps == (PageInterval(51, 99),)
    assert result.last_page_reached_with_gaps is True
    assert result.full_coverage_confirmed is False


def test_complete_coverage() -> None:
    result = calculate(100, (PageInterval(1, 100),), completed=True)
    assert result.remaining_pages == 0
    assert result.gaps == ()
    assert result.last_page_reached_with_gaps is False
    assert result.full_coverage_confirmed is True


def test_rejects_inconsistent_progress_and_coverage() -> None:
    coverage = ReadingCoverage((PageInterval(1, 10),))
    progress = ReadingProgress(BookId.new(), 100, 9, 10, Decimal("9.00"), False)
    with pytest.raises(ValueError):
        ReadingInsightsCalculator.calculate(progress, coverage)

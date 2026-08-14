from dataclasses import FrozenInstanceError

import pytest

from app.read.domain.models.page_interval import PageInterval
from app.read.domain.models.reading_coverage import ReadingCoverage


def test_empty_and_derived_metrics() -> None:
    empty = ReadingCoverage(())
    coverage = ReadingCoverage((PageInterval(1, 10), PageInterval(20, 25)))
    assert (empty.unique_pages_read, empty.highest_page_reached) == (0, None)
    assert (coverage.unique_pages_read, coverage.highest_page_reached) == (16, 25)


def test_requires_tuple_of_intervals() -> None:
    with pytest.raises(TypeError):
        ReadingCoverage([])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ReadingCoverage(((1, 2),))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "intervals",
    [
        (PageInterval(5, 10), PageInterval(1, 2)),
        (PageInterval(1, 5), PageInterval(5, 10)),
        (PageInterval(1, 5), PageInterval(6, 10)),
    ],
)
def test_rejects_unordered_overlapping_or_adjacent(intervals: tuple[PageInterval, ...]) -> None:
    with pytest.raises(ValueError):
        ReadingCoverage(intervals)


def test_is_frozen() -> None:
    coverage = ReadingCoverage(())
    with pytest.raises(FrozenInstanceError):
        coverage.covered_intervals = ()  # type: ignore[misc]

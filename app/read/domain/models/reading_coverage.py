from dataclasses import dataclass

from app.read.domain.models.page_interval import PageInterval


@dataclass(frozen=True)
class ReadingCoverage:
    covered_intervals: tuple[PageInterval, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.covered_intervals, tuple):
            raise TypeError("Covered intervals must be a tuple.")
        if not all(isinstance(interval, PageInterval) for interval in self.covered_intervals):
            raise TypeError("Covered intervals must contain PageInterval values.")
        for previous, current in zip(
            self.covered_intervals, self.covered_intervals[1:], strict=False
        ):
            if current.start_page <= previous.end_page + 1:
                raise ValueError("Covered intervals must be ordered, disjoint, and non-adjacent.")

    @property
    def unique_pages_read(self) -> int:
        return sum(interval.length for interval in self.covered_intervals)

    @property
    def highest_page_reached(self) -> int | None:
        if not self.covered_intervals:
            return None
        return self.covered_intervals[-1].end_page

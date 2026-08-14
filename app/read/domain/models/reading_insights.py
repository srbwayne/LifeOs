from dataclasses import dataclass

from app.read.domain.models.page_interval import PageInterval
from app.read.domain.value_objects.book_id import BookId


@dataclass(frozen=True)
class ReadingInsights:
    book_id: BookId
    remaining_pages: int
    gaps: tuple[PageInterval, ...]
    last_page_reached_with_gaps: bool
    full_coverage_confirmed: bool

    def __post_init__(self) -> None:
        if not isinstance(self.book_id, BookId):
            raise TypeError("Reading insights book ID must be a BookId.")
        if isinstance(self.remaining_pages, bool) or not isinstance(self.remaining_pages, int):
            raise TypeError("Remaining pages must be an integer.")
        if self.remaining_pages < 0:
            raise ValueError("Remaining pages must not be negative.")
        if not isinstance(self.gaps, tuple) or not all(
            isinstance(gap, PageInterval) for gap in self.gaps
        ):
            raise TypeError("Reading insight gaps must be a tuple of PageInterval values.")
        if not isinstance(self.last_page_reached_with_gaps, bool):
            raise TypeError("Last-page-with-gaps flag must be boolean.")
        if not isinstance(self.full_coverage_confirmed, bool):
            raise TypeError("Full-coverage flag must be boolean.")
        if self.full_coverage_confirmed and (
            self.remaining_pages != 0 or self.gaps or self.last_page_reached_with_gaps
        ):
            raise ValueError("Full coverage requires zero remaining pages and no gaps.")

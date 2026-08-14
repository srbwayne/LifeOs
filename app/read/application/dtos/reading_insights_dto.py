from __future__ import annotations

from dataclasses import dataclass

from app.read.domain.models.page_interval import PageInterval
from app.read.domain.models.reading_insights import ReadingInsights


@dataclass(frozen=True)
class PageIntervalDTO:
    start_page: int
    end_page: int

    @classmethod
    def from_interval(cls, interval: PageInterval) -> PageIntervalDTO:
        return cls(start_page=interval.start_page, end_page=interval.end_page)


@dataclass(frozen=True)
class ReadingInsightsDTO:
    book_id: str
    remaining_pages: int
    gaps: tuple[PageIntervalDTO, ...]
    last_page_reached_with_gaps: bool
    full_coverage_confirmed: bool

    @classmethod
    def from_insights(cls, insights: ReadingInsights) -> ReadingInsightsDTO:
        return cls(
            book_id=insights.book_id.to_persistence(),
            remaining_pages=insights.remaining_pages,
            gaps=tuple(PageIntervalDTO.from_interval(gap) for gap in insights.gaps),
            last_page_reached_with_gaps=insights.last_page_reached_with_gaps,
            full_coverage_confirmed=insights.full_coverage_confirmed,
        )

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ReadingStatisticsAggregateProjection:
    total_books: int
    books_with_reading_sessions: int
    total_reading_sessions: int
    total_pages_read: int


@dataclass(frozen=True)
class ReadingStatisticsDTO:
    total_books: int
    books_with_reading_sessions: int
    total_reading_sessions: int
    total_pages_read: int
    average_pages_per_session: Decimal

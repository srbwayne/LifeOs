from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.read.domain.models.reading_progress import ReadingProgress


@dataclass(frozen=True)
class ReadingProgressDTO:
    book_id: str
    total_pages: int
    unique_pages_read: int
    highest_page_reached: int | None
    percentage: Decimal
    completed: bool

    @classmethod
    def from_progress(cls, progress: ReadingProgress) -> ReadingProgressDTO:
        return cls(
            book_id=progress.book_id.to_persistence(),
            total_pages=progress.total_pages,
            unique_pages_read=progress.unique_pages_read,
            highest_page_reached=progress.highest_page_reached,
            percentage=progress.percentage,
            completed=progress.completed,
        )

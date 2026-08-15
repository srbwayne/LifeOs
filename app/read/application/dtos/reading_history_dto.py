from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReadingHistoryItemDTO:
    id: str
    book_id: str
    book_title: str
    start_page: int
    end_page: int
    pages_read: int
    started_at: datetime
    ended_at: datetime
    notes: str | None

    @classmethod
    def from_values(
        cls,
        *,
        id: str,
        book_id: str,
        book_title: str,
        start_page: int,
        end_page: int,
        started_at: datetime,
        ended_at: datetime,
        notes: str | None,
    ) -> ReadingHistoryItemDTO:
        return cls(
            id=id,
            book_id=book_id,
            book_title=book_title,
            start_page=start_page,
            end_page=end_page,
            pages_read=end_page - start_page + 1,
            started_at=started_at,
            ended_at=ended_at,
            notes=notes,
        )


@dataclass(frozen=True)
class ReadingHistoryPageDTO:
    items: tuple[ReadingHistoryItemDTO, ...]
    page: int
    size: int
    total_items: int
    total_pages: int

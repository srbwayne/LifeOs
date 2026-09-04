from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BookCompletionItemDTO:
    book_id: str
    book_title: str
    completed_at: datetime


@dataclass(frozen=True)
class BookCompletionPageDTO:
    items: tuple[BookCompletionItemDTO, ...]
    page: int
    size: int
    total_items: int
    total_pages: int

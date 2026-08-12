from dataclasses import dataclass
from decimal import Decimal

from app.read.domain.value_objects.book_id import BookId


@dataclass(frozen=True)
class ReadingProgress:
    book_id: BookId
    total_pages: int
    unique_pages_read: int
    highest_page_reached: int | None
    percentage: Decimal
    completed: bool

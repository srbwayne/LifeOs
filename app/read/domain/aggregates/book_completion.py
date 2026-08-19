from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.read.domain.errors.book_completion_errors import (
    InvalidBookCompletionTimeError,
)
from app.read.domain.value_objects.book_completion_id import BookCompletionId
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.aggregate import AggregateRoot


@dataclass(eq=False, frozen=True)
class BookCompletion(AggregateRoot):
    id: BookCompletionId
    book_id: BookId
    completed_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.id, BookCompletionId):
            raise TypeError("Book completion ID must be a BookCompletionId.")
        if not isinstance(self.book_id, BookId):
            raise TypeError("Book completion book must be a BookId.")

        object.__setattr__(self, "completed_at", self._normalize_datetime(self.completed_at))
        object.__setattr__(self, "_domain_events", [])

    @classmethod
    def create(cls, book_id: BookId, completed_at: datetime) -> BookCompletion:
        return cls._build(
            id=BookCompletionId.new(),
            book_id=book_id,
            completed_at=completed_at,
        )

    @classmethod
    def restore(
        cls,
        id: BookCompletionId,
        book_id: BookId,
        completed_at: datetime,
    ) -> BookCompletion:
        return cls._build(id=id, book_id=book_id, completed_at=completed_at)

    @classmethod
    def _build(
        cls,
        id: BookCompletionId,
        book_id: BookId,
        completed_at: datetime,
    ) -> BookCompletion:
        return cls(id=id, book_id=book_id, completed_at=completed_at)

    @staticmethod
    def _normalize_datetime(value: datetime) -> datetime:
        if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
            raise InvalidBookCompletionTimeError()
        return value.astimezone(timezone.utc)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BookCompletion):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'BookCompletion'")

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.read.domain.errors.reading_session_errors import (
    InvalidReadingRangeError,
    InvalidReadingSessionTimeError,
    ReadingBeyondBookError,
)
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.page_number import PageNumber
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.domain.value_objects.total_pages import TotalPages
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId


@dataclass(eq=False)
class ReadingSession(AggregateRoot):
    id: ReadingSessionId
    owner_id: UserId
    book_id: BookId
    start_page: PageNumber
    end_page: PageNumber
    started_at: datetime
    ended_at: datetime
    notes: str | None = None

    @classmethod
    def create(
        cls,
        owner_id: UserId,
        book_id: BookId,
        start_page: int,
        end_page: int,
        started_at: datetime,
        ended_at: datetime,
        book_total_pages: TotalPages,
        notes: str | None = None,
    ) -> ReadingSession:
        if not isinstance(book_total_pages, TotalPages):
            raise TypeError("Reading session book total pages must be a TotalPages.")

        start = PageNumber(start_page)
        end = PageNumber(end_page)
        if end.value > book_total_pages.value:
            raise ReadingBeyondBookError()

        return cls._build(
            id=ReadingSessionId.new(),
            owner_id=owner_id,
            book_id=book_id,
            start_page=start,
            end_page=end,
            started_at=started_at,
            ended_at=ended_at,
            notes=notes,
        )

    @classmethod
    def restore(
        cls,
        id: ReadingSessionId,
        owner_id: UserId,
        book_id: BookId,
        start_page: PageNumber,
        end_page: PageNumber,
        started_at: datetime,
        ended_at: datetime,
        notes: str | None = None,
    ) -> ReadingSession:
        if not isinstance(id, ReadingSessionId):
            raise TypeError("Reading session ID must be a ReadingSessionId.")
        if not isinstance(start_page, PageNumber) or not isinstance(end_page, PageNumber):
            raise TypeError("Reading session pages must be PageNumber values.")

        return cls._build(
            id=id,
            owner_id=owner_id,
            book_id=book_id,
            start_page=start_page,
            end_page=end_page,
            started_at=started_at,
            ended_at=ended_at,
            notes=notes,
        )

    @classmethod
    def _build(
        cls,
        id: ReadingSessionId,
        owner_id: UserId,
        book_id: BookId,
        start_page: PageNumber,
        end_page: PageNumber,
        started_at: datetime,
        ended_at: datetime,
        notes: str | None,
    ) -> ReadingSession:
        if not isinstance(owner_id, UserId):
            raise TypeError("Reading session owner must be a UserId.")
        if not isinstance(book_id, BookId):
            raise TypeError("Reading session book must be a BookId.")
        if end_page.value < start_page.value:
            raise InvalidReadingRangeError()

        normalized_started_at = cls._normalize_datetime(started_at)
        normalized_ended_at = cls._normalize_datetime(ended_at)
        if normalized_ended_at < normalized_started_at:
            raise InvalidReadingSessionTimeError()

        return cls(
            id=id,
            owner_id=owner_id,
            book_id=book_id,
            start_page=start_page,
            end_page=end_page,
            started_at=normalized_started_at,
            ended_at=normalized_ended_at,
            notes=cls._normalize_notes(notes),
        )

    @staticmethod
    def _normalize_datetime(value: datetime) -> datetime:
        if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
            raise InvalidReadingSessionTimeError()
        return value.astimezone(timezone.utc)

    @staticmethod
    def _normalize_notes(value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("Reading session notes must be a string or None.")
        return value.strip() or None

    @property
    def pages_read(self) -> int:
        return self.end_page.value - self.start_page.value + 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReadingSession):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'ReadingSession'")

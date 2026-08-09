from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.read.domain.aggregates.reading_session import ReadingSession


@dataclass(frozen=True)
class ReadingSessionDTO:
    id: str
    book_id: str
    start_page: int
    end_page: int
    pages_read: int
    started_at: datetime
    ended_at: datetime
    notes: str | None

    @classmethod
    def from_session(cls, session: ReadingSession) -> ReadingSessionDTO:
        return cls(
            id=session.id.to_persistence(),
            book_id=session.book_id.to_persistence(),
            start_page=session.start_page.value,
            end_page=session.end_page.value,
            pages_read=session.pages_read,
            started_at=session.started_at,
            ended_at=session.ended_at,
            notes=session.notes,
        )

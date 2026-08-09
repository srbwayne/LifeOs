from typing import Protocol

from app.read.domain.aggregates.reading_session import ReadingSession


class IReadingSessionRepository(Protocol):
    def save(self, session: ReadingSession) -> None: ...

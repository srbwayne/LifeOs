from typing import Protocol

from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


class IReadingSessionRepository(Protocol):
    def save(self, session: ReadingSession) -> None: ...

    def list_by_book_and_owner(
        self,
        book_id: BookId,
        owner_id: UserId,
    ) -> tuple[ReadingSession, ...]: ...

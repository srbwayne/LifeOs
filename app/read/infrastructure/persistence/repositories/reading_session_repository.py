from sqlalchemy import select
from sqlalchemy.orm import Session

from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.domain.value_objects.book_id import BookId
from app.read.infrastructure.persistence.mappers.reading_session_mapper import (
    ReadingSessionMapper,
)
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyReadingSessionRepository(IReadingSessionRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, session: ReadingSession) -> None:
        self._session.add(ReadingSessionMapper.to_persistence(session))

    def list_by_book_and_owner(
        self,
        book_id: BookId,
        owner_id: UserId,
    ) -> tuple[ReadingSession, ...]:
        statement = (
            select(ReadingSessionModel)
            .where(
                ReadingSessionModel.book_id == book_id.to_persistence(),
                ReadingSessionModel.user_id == owner_id.to_persistence(),
            )
            .order_by(
                ReadingSessionModel.start_page.asc(),
                ReadingSessionModel.end_page.asc(),
                ReadingSessionModel.id.asc(),
            )
        )
        models = self._session.scalars(statement).all()
        return tuple(ReadingSessionMapper.to_domain(model) for model in models)

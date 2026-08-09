from sqlalchemy.orm import Session

from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.infrastructure.persistence.mappers.reading_session_mapper import (
    ReadingSessionMapper,
)


class SqlAlchemyReadingSessionRepository(IReadingSessionRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, session: ReadingSession) -> None:
        self._session.add(ReadingSessionMapper.to_persistence(session))

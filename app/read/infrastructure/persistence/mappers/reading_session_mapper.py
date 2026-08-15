from datetime import datetime

from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.page_number import PageNumber
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.infrastructure.persistence.datetime import canonicalize_utc_datetime
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.shared.domain.identifiers.user_id import UserId


class ReadingSessionMapper:
    @staticmethod
    def to_domain(model: ReadingSessionModel) -> ReadingSession:
        return ReadingSession.restore(
            id=ReadingSessionId.from_value(model.id),
            owner_id=UserId.from_value(model.user_id),
            book_id=BookId.from_value(model.book_id),
            start_page=PageNumber(model.start_page),
            end_page=PageNumber(model.end_page),
            started_at=ReadingSessionMapper._as_utc(model.started_at),
            ended_at=ReadingSessionMapper._as_utc(model.ended_at),
            notes=model.notes,
        )

    @staticmethod
    def to_persistence(session: ReadingSession) -> ReadingSessionModel:
        return ReadingSessionModel(
            id=session.id.to_persistence(),
            user_id=session.owner_id.to_persistence(),
            book_id=session.book_id.to_persistence(),
            start_page=session.start_page.value,
            end_page=session.end_page.value,
            started_at=session.started_at,
            ended_at=session.ended_at,
            notes=session.notes,
        )

    @staticmethod
    def _as_utc(value: datetime) -> datetime:
        return canonicalize_utc_datetime(value)

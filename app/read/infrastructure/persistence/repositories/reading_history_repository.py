from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.read.application.dtos.reading_history_dto import ReadingHistoryItemDTO
from app.read.application.ports.reading_history_repository import (
    IReadingHistoryReadRepository,
)
from app.read.infrastructure.persistence.datetime import canonicalize_utc_datetime
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyReadingHistoryReadRepository(IReadingHistoryReadRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def count_by_owner(self, owner_id: UserId) -> int:
        owner = owner_id.to_persistence()
        statement = (
            select(func.count())
            .select_from(ReadingSessionModel)
            .join(
                BookModel,
                and_(
                    BookModel.id == ReadingSessionModel.book_id,
                    BookModel.user_id == ReadingSessionModel.user_id,
                ),
            )
            .where(
                ReadingSessionModel.user_id == owner,
                BookModel.user_id == owner,
            )
        )
        return int(self._session.scalar(statement) or 0)

    def list_page_by_owner(
        self,
        owner_id: UserId,
        offset: int,
        limit: int,
    ) -> tuple[ReadingHistoryItemDTO, ...]:
        owner = owner_id.to_persistence()
        statement = (
            select(
                ReadingSessionModel.id,
                ReadingSessionModel.book_id,
                BookModel.title.label("book_title"),
                ReadingSessionModel.start_page,
                ReadingSessionModel.end_page,
                ReadingSessionModel.started_at,
                ReadingSessionModel.ended_at,
                ReadingSessionModel.notes,
            )
            .join(
                BookModel,
                and_(
                    BookModel.id == ReadingSessionModel.book_id,
                    BookModel.user_id == ReadingSessionModel.user_id,
                ),
            )
            .where(
                ReadingSessionModel.user_id == owner,
                BookModel.user_id == owner,
            )
            .order_by(
                ReadingSessionModel.started_at.desc(),
                ReadingSessionModel.id.desc(),
            )
            .limit(limit)
            .offset(offset)
        )
        return tuple(
            ReadingHistoryItemDTO.from_values(
                id=row.id,
                book_id=row.book_id,
                book_title=row.book_title,
                start_page=row.start_page,
                end_page=row.end_page,
                started_at=canonicalize_utc_datetime(row.started_at),
                ended_at=canonicalize_utc_datetime(row.ended_at),
                notes=row.notes,
            )
            for row in self._session.execute(statement)
        )

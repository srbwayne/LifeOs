from sqlalchemy import and_, distinct, func, select
from sqlalchemy.orm import Session

from app.read.application.dtos.reading_statistics_dto import (
    ReadingStatisticsAggregateProjection,
)
from app.read.application.ports.reading_statistics_repository import (
    IReadingStatisticsReadRepository,
)
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyReadingStatisticsReadRepository(IReadingStatisticsReadRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_owner(self, owner_id: UserId) -> ReadingStatisticsAggregateProjection:
        owner = owner_id.to_persistence()
        total_books_statement = (
            select(func.count()).select_from(BookModel).where(BookModel.user_id == owner)
        )
        total_books = int(self._session.scalar(total_books_statement) or 0)

        aggregate_statement = (
            select(
                func.count(distinct(ReadingSessionModel.book_id)).label(
                    "books_with_reading_sessions"
                ),
                func.count().label("total_reading_sessions"),
                func.coalesce(
                    func.sum(ReadingSessionModel.end_page - ReadingSessionModel.start_page + 1),
                    0,
                ).label("total_pages_read"),
            )
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
        row = self._session.execute(aggregate_statement).one()
        return ReadingStatisticsAggregateProjection(
            total_books=total_books,
            books_with_reading_sessions=int(row.books_with_reading_sessions or 0),
            total_reading_sessions=int(row.total_reading_sessions or 0),
            total_pages_read=int(row.total_pages_read or 0),
        )

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.read.application.dtos.book_completion_dto import BookCompletionItemDTO
from app.read.application.ports.book_completion_read_repository import (
    IBookCompletionReadRepository,
)
from app.read.infrastructure.persistence.datetime import canonicalize_utc_datetime
from app.read.infrastructure.persistence.models.book_completion_model import (
    BookCompletionModel,
)
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyBookCompletionReadRepository(IBookCompletionReadRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def count_by_owner(self, owner_id: UserId) -> int:
        statement = (
            select(func.count())
            .select_from(BookCompletionModel)
            .join(BookModel, BookModel.id == BookCompletionModel.book_id)
            .where(BookModel.user_id == owner_id.to_persistence())
        )
        return int(self._session.scalar(statement) or 0)

    def list_page_by_owner(
        self,
        owner_id: UserId,
        offset: int,
        limit: int,
    ) -> tuple[BookCompletionItemDTO, ...]:
        statement = (
            select(
                BookCompletionModel.book_id,
                BookModel.title.label("book_title"),
                BookCompletionModel.completed_at,
            )
            .join(BookModel, BookModel.id == BookCompletionModel.book_id)
            .where(BookModel.user_id == owner_id.to_persistence())
            .order_by(
                BookCompletionModel.completed_at.desc(),
                BookCompletionModel.book_id.desc(),
            )
            .limit(limit)
            .offset(offset)
        )
        return tuple(
            BookCompletionItemDTO(
                book_id=row.book_id,
                book_title=row.book_title,
                completed_at=canonicalize_utc_datetime(row.completed_at),
            )
            for row in self._session.execute(statement)
        )

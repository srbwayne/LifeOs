from sqlalchemy import select
from sqlalchemy.orm import Session

from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.ports.book_completion_repository import IBookCompletionRepository
from app.read.domain.value_objects.book_id import BookId
from app.read.infrastructure.persistence.mappers.book_completion_mapper import (
    BookCompletionMapper,
)
from app.read.infrastructure.persistence.models.book_completion_model import (
    BookCompletionModel,
)
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyBookCompletionRepository(IBookCompletionRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, completion: BookCompletion) -> None:
        self._session.add(BookCompletionMapper.to_persistence(completion))

    def get_by_book_and_owner(
        self,
        book_id: BookId,
        owner_id: UserId,
    ) -> BookCompletion | None:
        statement = (
            select(BookCompletionModel)
            .join(BookModel, BookModel.id == BookCompletionModel.book_id)
            .where(
                BookCompletionModel.book_id == book_id.to_persistence(),
                BookModel.user_id == owner_id.to_persistence(),
            )
        )
        model = self._session.scalars(statement).one_or_none()
        return BookCompletionMapper.to_domain(model) if model is not None else None

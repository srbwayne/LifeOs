from sqlalchemy.orm import Session

from app.read.domain.aggregates.book import Book
from app.read.domain.ports.book_repository import IBookRepository
from app.read.infrastructure.persistence.mappers.book_mapper import BookMapper
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyBookRepository(IBookRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, book: Book) -> None:
        self._session.add(BookMapper.to_persistence(book))

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]:
        models = (
            self._session.query(BookModel)
            .filter_by(user_id=owner_id.to_persistence())
            .order_by(BookModel.id.asc())
            .all()
        )
        return tuple(BookMapper.to_domain(model) for model in models)

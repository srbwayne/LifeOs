from app.read.domain.aggregates.book import Book
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.total_pages import TotalPages
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.shared.domain.identifiers.user_id import UserId


class BookMapper:
    @staticmethod
    def to_domain(model: BookModel) -> Book:
        return Book.restore(
            id=BookId.from_value(model.id),
            owner_id=UserId.from_value(model.user_id),
            title=model.title,
            author=model.author,
            total_pages=TotalPages(model.total_pages),
            isbn=model.isbn,
            publisher=model.publisher,
            edition=model.edition,
            cover=model.cover,
            genre=model.genre,
            language=model.language,
        )

    @staticmethod
    def to_persistence(book: Book) -> BookModel:
        return BookModel(
            id=book.id.to_persistence(),
            user_id=book.owner_id.to_persistence(),
            title=book.title,
            author=book.author,
            total_pages=book.total_pages.value,
            isbn=book.isbn,
            publisher=book.publisher,
            edition=book.edition,
            cover=book.cover,
            genre=book.genre,
            language=book.language,
        )

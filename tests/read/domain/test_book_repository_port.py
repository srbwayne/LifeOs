from app.read.domain.aggregates.book import Book
from app.read.domain.ports.book_repository import IBookRepository
from app.shared.domain.identifiers.user_id import UserId


class BookRepositoryStub:
    def __init__(self) -> None:
        self.books: list[Book] = []

    def save(self, book: Book) -> None:
        self.books.append(book)

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]:
        return tuple(book for book in self.books if book.owner_id == owner_id)


def accepts_book_repository(repository: IBookRepository) -> IBookRepository:
    return repository


def test_repository_port_accepts_structural_implementation() -> None:
    repository = BookRepositoryStub()

    assert accepts_book_repository(repository) is repository

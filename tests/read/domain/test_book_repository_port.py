from app.read.domain.aggregates.book import Book
from app.read.domain.ports.book_repository import IBookRepository
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


class BookRepositoryStub:
    def __init__(self) -> None:
        self.books: list[Book] = []

    def save(self, book: Book) -> None:
        self.books.append(book)

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]:
        return tuple(book for book in self.books if book.owner_id == owner_id)

    def get_by_id_and_owner(self, book_id: BookId, owner_id: UserId) -> Book | None:
        return next(
            (book for book in self.books if book.id == book_id and book.owner_id == owner_id),
            None,
        )


def accepts_book_repository(repository: IBookRepository) -> IBookRepository:
    return repository


def test_repository_port_accepts_structural_implementation() -> None:
    repository = BookRepositoryStub()

    assert accepts_book_repository(repository) is repository


def test_repository_port_defines_only_authorized_operations() -> None:
    public_operations = {
        name
        for name, value in IBookRepository.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert public_operations == {"save", "list_by_owner", "get_by_id_and_owner"}

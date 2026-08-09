from dataclasses import dataclass

from app.read.application.dtos.book_dto import BookDTO
from app.read.domain.aggregates.book import Book
from app.read.domain.ports.book_repository import IBookRepository
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class CreateBookCommand:
    owner_id: UserId
    title: str
    author: str
    total_pages: int
    isbn: str | None = None
    publisher: str | None = None
    edition: str | None = None
    cover: str | None = None
    genre: str | None = None
    language: str | None = None


class CreateBookCommandHandler:
    def __init__(self, repository: IBookRepository, unit_of_work: IUnitOfWork) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: CreateBookCommand) -> BookDTO:
        with self._unit_of_work as uow:
            book = Book.create(
                owner_id=command.owner_id,
                title=command.title,
                author=command.author,
                total_pages=command.total_pages,
                isbn=command.isbn,
                publisher=command.publisher,
                edition=command.edition,
                cover=command.cover,
                genre=command.genre,
                language=command.language,
            )
            self._repository.save(book)
            uow.commit()
        return BookDTO.from_book(book)

from dataclasses import dataclass

from app.read.application.dtos.book_dto import BookDTO
from app.read.domain.ports.book_repository import IBookRepository
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ListMyBooksQuery:
    owner_id: UserId


class ListMyBooksQueryHandler:
    def __init__(self, repository: IBookRepository) -> None:
        self._repository = repository

    def __call__(self, query: ListMyBooksQuery) -> tuple[BookDTO, ...]:
        books = self._repository.list_by_owner(query.owner_id)
        return tuple(BookDTO.from_book(book) for book in books)

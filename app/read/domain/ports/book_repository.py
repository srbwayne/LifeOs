from typing import Protocol

from app.read.domain.aggregates.book import Book
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


class IBookRepository(Protocol):
    def save(self, book: Book) -> None: ...

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]: ...

    def get_by_id_and_owner(self, book_id: BookId, owner_id: UserId) -> Book | None: ...

from typing import Protocol

from app.read.domain.aggregates.book import Book
from app.shared.domain.identifiers.user_id import UserId


class IBookRepository(Protocol):
    def save(self, book: Book) -> None: ...

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]: ...

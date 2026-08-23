from typing import Protocol

from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


class IBookCompletionRepository(Protocol):
    def save(self, completion: BookCompletion) -> None: ...

    def get_by_book_and_owner(
        self,
        book_id: BookId,
        owner_id: UserId,
    ) -> BookCompletion | None: ...

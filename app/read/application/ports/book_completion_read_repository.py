from typing import Protocol

from app.read.application.dtos.book_completion_dto import BookCompletionItemDTO
from app.shared.domain.identifiers.user_id import UserId


class IBookCompletionReadRepository(Protocol):
    def count_by_owner(self, owner_id: UserId) -> int: ...

    def list_page_by_owner(
        self,
        owner_id: UserId,
        offset: int,
        limit: int,
    ) -> tuple[BookCompletionItemDTO, ...]: ...

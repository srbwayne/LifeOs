from dataclasses import dataclass

from app.read.application.dtos.book_completion_dto import BookCompletionPageDTO
from app.read.application.ports.book_completion_read_repository import (
    IBookCompletionReadRepository,
)
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ListBookCompletionsQuery:
    owner_id: UserId
    page: int
    size: int


class ListBookCompletionsQueryHandler:
    def __init__(self, repository: IBookCompletionReadRepository) -> None:
        self._repository = repository

    def __call__(self, query: ListBookCompletionsQuery) -> BookCompletionPageDTO:
        total_items = self._repository.count_by_owner(query.owner_id)
        offset = (query.page - 1) * query.size
        items = self._repository.list_page_by_owner(
            query.owner_id,
            offset,
            query.size,
        )
        total_pages = (total_items + query.size - 1) // query.size if total_items else 0
        return BookCompletionPageDTO(
            items=items,
            page=query.page,
            size=query.size,
            total_items=total_items,
            total_pages=total_pages,
        )

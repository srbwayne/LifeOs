from dataclasses import dataclass

from app.read.application.dtos.reading_history_dto import ReadingHistoryPageDTO
from app.read.application.ports.reading_history_repository import (
    IReadingHistoryReadRepository,
)
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ListReadingHistoryQuery:
    owner_id: UserId
    page: int
    size: int


class ListReadingHistoryQueryHandler:
    def __init__(self, repository: IReadingHistoryReadRepository) -> None:
        self._repository = repository

    def __call__(self, query: ListReadingHistoryQuery) -> ReadingHistoryPageDTO:
        total_items = self._repository.count_by_owner(query.owner_id)
        offset = (query.page - 1) * query.size
        items = self._repository.list_page_by_owner(
            query.owner_id,
            offset,
            query.size,
        )
        total_pages = (total_items + query.size - 1) // query.size if total_items else 0
        return ReadingHistoryPageDTO(
            items=items,
            page=query.page,
            size=query.size,
            total_items=total_items,
            total_pages=total_pages,
        )

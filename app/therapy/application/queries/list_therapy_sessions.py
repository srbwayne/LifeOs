from dataclasses import dataclass

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapy_session_dto import TherapySessionHistoryPageDTO
from app.therapy.application.ports.therapy_session_read_repository import (
    ITherapySessionReadRepository,
)


@dataclass(frozen=True)
class ListTherapySessionsQuery:
    owner_id: UserId
    page: int
    size: int


class ListTherapySessionsQueryHandler:
    def __init__(self, repository: ITherapySessionReadRepository) -> None:
        self._repository = repository

    def __call__(self, query: ListTherapySessionsQuery) -> TherapySessionHistoryPageDTO:
        total = self._repository.count_by_owner(query.owner_id)
        items = self._repository.list_page_by_owner(
            query.owner_id, (query.page - 1) * query.size, query.size
        )
        pages = (total + query.size - 1) // query.size if total else 0
        return TherapySessionHistoryPageDTO(items, query.page, query.size, total, pages)

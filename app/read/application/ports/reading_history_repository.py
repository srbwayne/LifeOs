from typing import Protocol

from app.read.application.dtos.reading_history_dto import ReadingHistoryItemDTO
from app.shared.domain.identifiers.user_id import UserId


class IReadingHistoryReadRepository(Protocol):
    def count_by_owner(self, owner_id: UserId) -> int: ...

    def list_page_by_owner(
        self,
        owner_id: UserId,
        offset: int,
        limit: int,
    ) -> tuple[ReadingHistoryItemDTO, ...]: ...

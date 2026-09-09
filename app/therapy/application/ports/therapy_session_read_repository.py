from typing import Protocol

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapy_session_dto import (
    TherapySessionDetailDTO,
    TherapySessionHistoryItemDTO,
)
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId


class ITherapySessionReadRepository(Protocol):
    def get_by_id_and_owner(
        self,
        session_id: TherapySessionId,
        owner_id: UserId,
    ) -> TherapySessionDetailDTO | None: ...

    def count_by_owner(self, owner_id: UserId) -> int: ...

    def list_page_by_owner(
        self,
        owner_id: UserId,
        offset: int,
        limit: int,
    ) -> tuple[TherapySessionHistoryItemDTO, ...]: ...

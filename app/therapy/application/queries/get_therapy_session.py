from dataclasses import dataclass

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapy_session_dto import TherapySessionDetailDTO
from app.therapy.application.errors import TherapySessionNotFoundError
from app.therapy.application.ports.therapy_session_read_repository import (
    ITherapySessionReadRepository,
)
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId


@dataclass(frozen=True)
class GetTherapySessionQuery:
    owner_id: UserId
    session_id: TherapySessionId


class GetTherapySessionQueryHandler:
    def __init__(self, repository: ITherapySessionReadRepository) -> None:
        self._repository = repository

    def __call__(self, query: GetTherapySessionQuery) -> TherapySessionDetailDTO:
        result = self._repository.get_by_id_and_owner(query.session_id, query.owner_id)
        if result is None:
            raise TherapySessionNotFoundError()
        return result

from typing import Protocol

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapist_dto import TherapistDTO


class ITherapistReadRepository(Protocol):
    def list_by_owner(self, owner_id: UserId) -> tuple[TherapistDTO, ...]: ...

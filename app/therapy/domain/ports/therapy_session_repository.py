from typing import Protocol

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.aggregates.therapy_session import TherapySession
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId


class ITherapySessionRepository(Protocol):
    def save(self, session: TherapySession) -> None: ...

    def get_by_id_and_owner(
        self,
        session_id: TherapySessionId,
        owner_id: UserId,
    ) -> TherapySession | None: ...

    def delete(self, session: TherapySession) -> None: ...

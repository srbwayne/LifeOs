import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.aggregates.therapy_session import TherapySession
from app.therapy.domain.ports.therapy_session_repository import ITherapySessionRepository
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId
from app.therapy.infrastructure.persistence.mappers.therapy_session_mapper import (
    TherapySessionMapper,
)
from app.therapy.infrastructure.persistence.models.therapy_session_model import (
    TherapySessionModel,
)


class SqlAlchemyTherapySessionRepository(ITherapySessionRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, therapy_session: TherapySession) -> None:
        model = TherapySessionMapper.to_persistence(therapy_session)
        existing = self._session.get(TherapySessionModel, model.id)
        if existing is None:
            self._session.add(model)
            return
        existing.user_id = model.user_id
        existing.therapist_id = model.therapist_id
        existing.occurred_at = model.occurred_at
        existing.private_note = model.private_note
        existing.updated_at = datetime.datetime.now()

    def get_by_id_and_owner(
        self,
        session_id: TherapySessionId,
        owner_id: UserId,
    ) -> TherapySession | None:
        statement = select(TherapySessionModel).where(
            TherapySessionModel.id == session_id.to_persistence(),
            TherapySessionModel.user_id == owner_id.to_persistence(),
        )
        model = self._session.scalar(statement)
        return TherapySessionMapper.to_domain(model) if model is not None else None

    def delete(self, therapy_session: TherapySession) -> None:
        statement = select(TherapySessionModel).where(
            TherapySessionModel.id == therapy_session.id.to_persistence(),
            TherapySessionModel.user_id == therapy_session.owner_id.to_persistence(),
        )
        model = self._session.scalar(statement)
        if model is not None:
            self._session.delete(model)

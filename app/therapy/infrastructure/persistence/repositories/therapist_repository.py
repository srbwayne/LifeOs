import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.ports.therapist_repository import ITherapistRepository
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.infrastructure.persistence.mappers.therapist_mapper import TherapistMapper
from app.therapy.infrastructure.persistence.models.therapist_model import TherapistModel


class SqlAlchemyTherapistRepository(ITherapistRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, therapist: Therapist) -> None:
        model = TherapistMapper.to_persistence(therapist)
        existing = self._session.get(TherapistModel, model.id)
        if existing is None:
            self._session.add(model)
            return
        existing.user_id = model.user_id
        existing.name = model.name
        existing.active = model.active
        existing.updated_at = datetime.datetime.now()

    def get_by_id_and_owner(
        self,
        therapist_id: TherapistId,
        owner_id: UserId,
    ) -> Therapist | None:
        statement = select(TherapistModel).where(
            TherapistModel.id == therapist_id.to_persistence(),
            TherapistModel.user_id == owner_id.to_persistence(),
        )
        model = self._session.scalar(statement)
        return TherapistMapper.to_domain(model) if model is not None else None

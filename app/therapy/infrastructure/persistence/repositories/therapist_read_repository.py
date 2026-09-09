from sqlalchemy import select
from sqlalchemy.orm import Session

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapist_dto import TherapistDTO
from app.therapy.application.ports.therapist_read_repository import ITherapistReadRepository
from app.therapy.infrastructure.persistence.models.therapist_model import TherapistModel


class SqlAlchemyTherapistReadRepository(ITherapistReadRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_owner(self, owner_id: UserId) -> tuple[TherapistDTO, ...]:
        statement = (
            select(TherapistModel.id, TherapistModel.name, TherapistModel.active)
            .where(TherapistModel.user_id == owner_id.to_persistence())
            .order_by(TherapistModel.name.asc(), TherapistModel.id.asc())
        )
        return tuple(
            TherapistDTO(id=row.id, name=row.name, active=row.active)
            for row in self._session.execute(statement)
        )

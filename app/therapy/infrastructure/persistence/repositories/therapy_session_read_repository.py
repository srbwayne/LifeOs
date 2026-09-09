from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapy_session_dto import (
    TherapySessionDetailDTO,
    TherapySessionHistoryItemDTO,
)
from app.therapy.application.ports.therapy_session_read_repository import (
    ITherapySessionReadRepository,
)
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId
from app.therapy.infrastructure.persistence.datetime import canonicalize_utc_datetime
from app.therapy.infrastructure.persistence.models.therapist_model import TherapistModel
from app.therapy.infrastructure.persistence.models.therapy_session_model import (
    TherapySessionModel,
)


class SqlAlchemyTherapySessionReadRepository(ITherapySessionReadRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def _owner_join(self):
        return and_(
            TherapistModel.id == TherapySessionModel.therapist_id,
            TherapistModel.user_id == TherapySessionModel.user_id,
        )

    def get_by_id_and_owner(
        self,
        session_id: TherapySessionId,
        owner_id: UserId,
    ) -> TherapySessionDetailDTO | None:
        statement = (
            select(
                TherapySessionModel.id,
                TherapySessionModel.therapist_id,
                TherapistModel.name,
                TherapySessionModel.occurred_at,
                TherapySessionModel.private_note,
            )
            .join(TherapistModel, self._owner_join())
            .where(
                TherapySessionModel.id == session_id.to_persistence(),
                TherapySessionModel.user_id == owner_id.to_persistence(),
            )
        )
        row = self._session.execute(statement).one_or_none()
        if row is None:
            return None
        return TherapySessionDetailDTO(
            id=row.id,
            therapist_id=row.therapist_id,
            therapist_name=row.name,
            occurred_at=canonicalize_utc_datetime(row.occurred_at),
            private_note=row.private_note,
        )

    def count_by_owner(self, owner_id: UserId) -> int:
        statement = (
            select(func.count())
            .select_from(TherapySessionModel)
            .where(TherapySessionModel.user_id == owner_id.to_persistence())
        )
        return int(self._session.scalar(statement) or 0)

    def list_page_by_owner(
        self,
        owner_id: UserId,
        offset: int,
        limit: int,
    ) -> tuple[TherapySessionHistoryItemDTO, ...]:
        statement = (
            select(
                TherapySessionModel.id,
                TherapySessionModel.therapist_id,
                TherapistModel.name,
                TherapySessionModel.occurred_at,
            )
            .join(TherapistModel, self._owner_join())
            .where(TherapySessionModel.user_id == owner_id.to_persistence())
            .order_by(
                TherapySessionModel.occurred_at.desc(),
                TherapySessionModel.id.desc(),
            )
            .offset(offset)
            .limit(limit)
        )
        return tuple(
            TherapySessionHistoryItemDTO(
                id=row.id,
                therapist_id=row.therapist_id,
                therapist_name=row.name,
                occurred_at=canonicalize_utc_datetime(row.occurred_at),
            )
            for row in self._session.execute(statement)
        )

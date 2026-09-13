from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.habits.application.dtos.habit_checklist_dto import HabitChecklistItemDTO
from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.ports.habit_read_repository import IHabitReadRepository
from app.habits.infrastructure.persistence.models.habit_completion_model import (
    HabitCompletionModel,
)
from app.habits.infrastructure.persistence.models.habit_model import HabitModel
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyHabitReadRepository(IHabitReadRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_owner(self, owner_id: UserId) -> tuple[HabitDTO, ...]:
        statement = (
            select(
                HabitModel.id,
                HabitModel.name,
                HabitModel.description,
                HabitModel.active,
            )
            .where(HabitModel.user_id == owner_id.to_persistence())
            .order_by(HabitModel.name.asc(), HabitModel.id.asc())
        )
        return tuple(
            HabitDTO(
                id=row.id,
                name=row.name,
                description=row.description,
                active=row.active,
            )
            for row in self._session.execute(statement)
        )

    def get_checklist_by_owner_and_record_date(
        self, owner_id: UserId, record_date: date
    ) -> tuple[HabitChecklistItemDTO, ...]:
        statement = (
            select(
                HabitModel.id,
                HabitModel.name,
                HabitModel.description,
                HabitCompletionModel.id.label("completion_id"),
            )
            .select_from(HabitModel)
            .outerjoin(
                HabitCompletionModel,
                (HabitCompletionModel.user_id == HabitModel.user_id)
                & (HabitCompletionModel.habit_id == HabitModel.id)
                & (HabitCompletionModel.record_date == record_date),
            )
            .where(
                HabitModel.user_id == owner_id.to_persistence(),
                HabitModel.active.is_(True),
            )
            .order_by(HabitModel.name.asc(), HabitModel.id.asc())
        )
        return tuple(
            HabitChecklistItemDTO(
                id=row.id,
                name=row.name,
                description=row.description,
                completed=row.completion_id is not None,
            )
            for row in self._session.execute(statement)
        )

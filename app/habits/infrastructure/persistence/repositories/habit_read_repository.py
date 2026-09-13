from sqlalchemy import select
from sqlalchemy.orm import Session

from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.ports.habit_read_repository import IHabitReadRepository
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

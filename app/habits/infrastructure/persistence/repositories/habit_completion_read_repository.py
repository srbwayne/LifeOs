from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.habits.application.dtos.habit_completion_dto import (
    HabitCompletionDTO,
    HabitCompletionPageDTO,
)
from app.habits.application.ports.habit_completion_read_repository import (
    IHabitCompletionReadRepository,
)
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.infrastructure.persistence.models.habit_completion_model import (
    HabitCompletionModel,
)
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyHabitCompletionReadRepository(IHabitCompletionReadRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_owner_and_habit(
        self,
        owner_id: UserId,
        habit_id: HabitId,
        page: int,
        size: int,
    ) -> HabitCompletionPageDTO:
        owner = owner_id.to_persistence()
        habit = habit_id.to_persistence()
        total_items = int(
            self._session.scalar(
                select(func.count())
                .select_from(HabitCompletionModel)
                .where(
                    HabitCompletionModel.user_id == owner,
                    HabitCompletionModel.habit_id == habit,
                )
            )
            or 0
        )
        statement = (
            select(
                HabitCompletionModel.id,
                HabitCompletionModel.habit_id,
                HabitCompletionModel.record_date,
            )
            .where(
                HabitCompletionModel.user_id == owner,
                HabitCompletionModel.habit_id == habit,
            )
            .order_by(
                HabitCompletionModel.record_date.desc(),
                HabitCompletionModel.id.desc(),
            )
            .limit(size)
            .offset((page - 1) * size)
        )
        items = tuple(
            HabitCompletionDTO(
                id=row.id,
                habit_id=row.habit_id,
                record_date=row.record_date,
            )
            for row in self._session.execute(statement)
        )
        total_pages = (total_items + size - 1) // size if total_items else 0
        return HabitCompletionPageDTO(items, page, size, total_items, total_pages)

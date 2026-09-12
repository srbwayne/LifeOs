from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.domain.ports.habit_completion_repository import IHabitCompletionRepository
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.infrastructure.persistence.mappers.habit_completion_mapper import (
    HabitCompletionMapper,
)
from app.habits.infrastructure.persistence.models.habit_completion_model import (
    HabitCompletionModel,
)
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyHabitCompletionRepository(IHabitCompletionRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, completion: HabitCompletion) -> None:
        model = HabitCompletionMapper.to_persistence(completion)
        existing = self._session.get(HabitCompletionModel, model.id)
        if existing is None:
            self._session.add(model)
            return

        if (
            existing.user_id != model.user_id
            or existing.habit_id != model.habit_id
            or existing.record_date != model.record_date
        ):
            raise ValueError("HabitCompletion immutable persistence fields conflict")

    def get_by_owner_habit_date(
        self,
        owner_id: UserId,
        habit_id: HabitId,
        record_date: date,
    ) -> HabitCompletion | None:
        statement = select(HabitCompletionModel).where(
            HabitCompletionModel.user_id == owner_id.to_persistence(),
            HabitCompletionModel.habit_id == habit_id.to_persistence(),
            HabitCompletionModel.record_date == record_date,
        )
        model = self._session.scalar(statement)
        return HabitCompletionMapper.to_domain(model) if model is not None else None

    def delete(self, completion: HabitCompletion) -> None:
        statement = select(HabitCompletionModel).where(
            HabitCompletionModel.id == completion.id.to_persistence(),
            HabitCompletionModel.user_id == completion.owner_id.to_persistence(),
            HabitCompletionModel.habit_id == completion.habit_id.to_persistence(),
        )
        model = self._session.scalar(statement)
        if model is not None:
            self._session.delete(model)

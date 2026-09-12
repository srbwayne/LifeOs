import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.ports.habit_repository import IHabitRepository
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.infrastructure.persistence.mappers.habit_mapper import HabitMapper
from app.habits.infrastructure.persistence.models.habit_model import HabitModel
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyHabitRepository(IHabitRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, habit: Habit) -> None:
        model = HabitMapper.to_persistence(habit)
        existing = self._session.get(HabitModel, model.id)
        if existing is None:
            self._session.add(model)
            return

        if (
            existing.user_id != model.user_id
            or existing.name != model.name
            or existing.description != model.description
        ):
            raise ValueError("Habit immutable persistence fields conflict")

        existing.active = model.active
        existing.updated_at = datetime.datetime.now()

    def get_by_id_and_owner(
        self,
        habit_id: HabitId,
        owner_id: UserId,
    ) -> Habit | None:
        statement = select(HabitModel).where(
            HabitModel.id == habit_id.to_persistence(),
            HabitModel.user_id == owner_id.to_persistence(),
        )
        model = self._session.scalar(statement)
        return HabitMapper.to_domain(model) if model is not None else None

    def get_by_owner_and_name(
        self,
        owner_id: UserId,
        name: str,
    ) -> Habit | None:
        statement = select(HabitModel).where(
            HabitModel.user_id == owner_id.to_persistence(),
            HabitModel.name == name,
        )
        model = self._session.scalar(statement)
        return HabitMapper.to_domain(model) if model is not None else None

from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.domain.value_objects.habit_completion_id import HabitCompletionId
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.infrastructure.persistence.models.habit_completion_model import (
    HabitCompletionModel,
)
from app.shared.domain.identifiers.user_id import UserId


class HabitCompletionMapper:
    @staticmethod
    def to_domain(model: HabitCompletionModel) -> HabitCompletion:
        return HabitCompletion.restore(
            id=HabitCompletionId.from_value(model.id),
            owner_id=UserId.from_value(model.user_id),
            habit_id=HabitId.from_value(model.habit_id),
            record_date=model.record_date,
        )

    @staticmethod
    def to_persistence(entity: HabitCompletion) -> HabitCompletionModel:
        return HabitCompletionModel(
            id=entity.id.to_persistence(),
            user_id=entity.owner_id.to_persistence(),
            habit_id=entity.habit_id.to_persistence(),
            record_date=entity.record_date,
        )

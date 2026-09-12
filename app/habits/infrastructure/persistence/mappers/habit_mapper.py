from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.infrastructure.persistence.models.habit_model import HabitModel
from app.shared.domain.identifiers.user_id import UserId


class HabitMapper:
    @staticmethod
    def to_domain(model: HabitModel) -> Habit:
        return Habit.restore(
            id=HabitId.from_value(model.id),
            owner_id=UserId.from_value(model.user_id),
            name=model.name,
            description=model.description,
            active=model.active,
        )

    @staticmethod
    def to_persistence(entity: Habit) -> HabitModel:
        return HabitModel(
            id=entity.id.to_persistence(),
            user_id=entity.owner_id.to_persistence(),
            name=entity.name,
            description=entity.description,
            active=entity.active,
        )

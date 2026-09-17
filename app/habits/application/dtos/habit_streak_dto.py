from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HabitStreakDTO:
    habit_id: str
    current_streak: int | None
    evaluation_date: date

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HabitCompletionDTO:
    id: str
    habit_id: str
    record_date: date

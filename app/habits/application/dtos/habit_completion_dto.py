from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HabitCompletionDTO:
    id: str
    habit_id: str
    record_date: date


@dataclass(frozen=True)
class HabitCompletionPageDTO:
    items: tuple[HabitCompletionDTO, ...]
    page: int
    size: int
    total_items: int
    total_pages: int

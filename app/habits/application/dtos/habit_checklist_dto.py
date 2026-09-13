from dataclasses import dataclass


@dataclass(frozen=True)
class HabitChecklistItemDTO:
    id: str
    name: str
    description: str | None
    completed: bool

from dataclasses import dataclass


@dataclass(frozen=True)
class HabitDTO:
    id: str
    name: str
    description: str | None
    active: bool

from dataclasses import dataclass


@dataclass(frozen=True)
class TherapistDTO:
    id: str
    name: str
    active: bool

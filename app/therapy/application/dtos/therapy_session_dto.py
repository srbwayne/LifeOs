from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TherapySessionHistoryItemDTO:
    id: str
    therapist_id: str
    therapist_name: str
    occurred_at: datetime


@dataclass(frozen=True)
class TherapySessionDetailDTO:
    id: str
    therapist_id: str
    therapist_name: str
    occurred_at: datetime
    private_note: str | None

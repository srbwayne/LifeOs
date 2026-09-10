from dataclasses import dataclass, field
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
    private_note: str | None = field(repr=False)


@dataclass(frozen=True)
class TherapySessionHistoryPageDTO:
    items: tuple[TherapySessionHistoryItemDTO, ...]
    page: int
    size: int
    total_items: int
    total_pages: int


@dataclass(frozen=True)
class TherapySessionPrivateNoteDTO:
    id: str
    private_note: str | None = field(repr=False)

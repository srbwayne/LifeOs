from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ProgressionDeliveryIntent:
    id: str
    reading_session_id: ReadingSessionId
    owner_id: UserId
    pages_read: int
    status: str = "PENDING"
    attempt_count: int = 0
    last_error: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_attempt_at: datetime | None = None
    delivered_at: datetime | None = None


class ProgressionDeliveryRepository(Protocol):
    def save(self, intent: ProgressionDeliveryIntent) -> None: ...

    def get_by_id(self, delivery_id: str) -> ProgressionDeliveryIntent | None: ...

    def get_by_reading_session_id(
        self, reading_session_id: ReadingSessionId
    ) -> ProgressionDeliveryIntent | None: ...

    def list_unresolved(self) -> tuple[ProgressionDeliveryIntent, ...]: ...

    def has_older_blocking(self, delivery_id: str) -> bool: ...

    def mark_delivered(self, delivery_id: str, delivered_at: datetime) -> None: ...

    def mark_failed(self, delivery_id: str, attempt_at: datetime, error: str) -> None: ...

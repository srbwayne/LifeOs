from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class ProgressionDeliveryIntent:
    id: str
    reading_session_id: str
    source: str
    idempotency_key: str
    subject_namespace: str
    subject_external_id: str
    configuration_key: str
    configuration_revision: int
    pages_read: int
    status: str = "PENDING"
    attempt_count: int = 0
    created_at: datetime | None = None
    last_attempt_at: datetime | None = None
    delivered_at: datetime | None = None
    last_error: str | None = None


class ProgressionDeliveryRepository(Protocol):
    def save(self, intent: ProgressionDeliveryIntent) -> None: ...

    def get_by_id(self, delivery_id: str) -> ProgressionDeliveryIntent | None: ...

    def list_unresolved(self) -> tuple[ProgressionDeliveryIntent, ...]: ...

    def mark_delivered(self, delivery_id: str, delivered_at: datetime) -> None: ...

    def mark_failed(
        self,
        delivery_id: str,
        attempt_at: datetime,
        error: str,
    ) -> None: ...

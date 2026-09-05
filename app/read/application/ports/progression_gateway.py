from dataclasses import dataclass
from typing import Protocol

from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ReadingProgressionFact:
    source_event_id: str
    user_id: UserId
    pages_read: int


@dataclass(frozen=True)
class ProgressionDeliveryResult:
    success: bool
    status_code: int | None = None
    error: str | None = None


class ProgressionGateway(Protocol):
    def evaluate_reading_session(
        self, fact: ReadingProgressionFact
    ) -> ProgressionDeliveryResult: ...

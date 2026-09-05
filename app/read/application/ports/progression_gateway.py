from dataclasses import dataclass
from typing import Protocol

from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class ReadingProgressionOccurrence:
    owner_id: UserId
    reading_session_id: ReadingSessionId
    pages_read: int


class ProgressionGatewayError(Exception):
    """Expected failure while delivering a committed progression occurrence."""


class ProgressionGateway(Protocol):
    def record(self, occurrence: ReadingProgressionOccurrence) -> None: ...

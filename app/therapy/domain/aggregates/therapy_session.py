from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.errors.therapy_errors import (
    InvalidPrivateNoteError,
    InvalidTherapySessionTimeError,
)
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId

PRIVATE_NOTE_MAX_LENGTH = 10_000


@dataclass(eq=False)
class TherapySession(AggregateRoot):
    id: TherapySessionId
    owner_id: UserId
    therapist_id: TherapistId
    occurred_at: datetime
    private_note: str | None

    @classmethod
    def create(
        cls,
        owner_id: UserId,
        therapist_id: TherapistId,
        occurred_at: datetime,
        now: datetime,
        private_note: str | None = None,
    ) -> TherapySession:
        return cls._build(
            id=TherapySessionId.new(),
            owner_id=owner_id,
            therapist_id=therapist_id,
            occurred_at=occurred_at,
            private_note=private_note,
            now=now,
            validate_future=True,
        )

    @classmethod
    def restore(
        cls,
        id: TherapySessionId,
        owner_id: UserId,
        therapist_id: TherapistId,
        occurred_at: datetime,
        private_note: str | None = None,
    ) -> TherapySession:
        if not isinstance(id, TherapySessionId):
            raise TypeError("Therapy session ID must be a TherapySessionId.")
        return cls._build(
            id=id,
            owner_id=owner_id,
            therapist_id=therapist_id,
            occurred_at=occurred_at,
            private_note=private_note,
            now=None,
            validate_future=False,
        )

    @classmethod
    def _build(
        cls,
        id: TherapySessionId,
        owner_id: UserId,
        therapist_id: TherapistId,
        occurred_at: datetime,
        private_note: str | None,
        now: datetime | None,
        validate_future: bool,
    ) -> TherapySession:
        if not isinstance(owner_id, UserId):
            raise TypeError("Therapy session owner must be a UserId.")
        if not isinstance(therapist_id, TherapistId):
            raise TypeError("Therapy session therapist must be a TherapistId.")

        normalized_occurred_at = cls._normalize_datetime(occurred_at)
        if validate_future:
            if now is None:
                raise TypeError("Therapy session creation requires a current UTC instant.")
            normalized_now = cls._normalize_datetime(now)
            if normalized_occurred_at > normalized_now:
                raise InvalidTherapySessionTimeError()

        return cls(
            id=id,
            owner_id=owner_id,
            therapist_id=therapist_id,
            occurred_at=normalized_occurred_at,
            private_note=cls._normalize_private_note(private_note),
        )

    @staticmethod
    def _normalize_datetime(value: datetime) -> datetime:
        if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
            raise InvalidTherapySessionTimeError()
        return value.astimezone(timezone.utc)

    @staticmethod
    def _normalize_private_note(value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise InvalidPrivateNoteError()
        normalized = value.strip()
        if len(normalized) > PRIVATE_NOTE_MAX_LENGTH:
            raise InvalidPrivateNoteError()
        return normalized or None

    def update_private_note(self, note: str | None) -> None:
        self.private_note = self._normalize_private_note(note)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TherapySession):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'TherapySession'")

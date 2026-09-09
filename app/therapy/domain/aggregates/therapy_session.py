from __future__ import annotations

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


class TherapySession(AggregateRoot):
    """Owner-scoped historical TherapySession aggregate root."""

    def __init__(
        self,
        id: TherapySessionId,
        owner_id: UserId,
        therapist_id: TherapistId,
        occurred_at: datetime,
        private_note: str | None,
    ) -> None:
        super().__init__()
        if not isinstance(id, TherapySessionId):
            raise TypeError("Therapy session ID must be a TherapySessionId.")
        if not isinstance(owner_id, UserId):
            raise TypeError("Therapy session owner must be a UserId.")
        if not isinstance(therapist_id, TherapistId):
            raise TypeError("Therapy session therapist must be a TherapistId.")
        self._id = id
        self._owner_id = owner_id
        self._therapist_id = therapist_id
        self._occurred_at = self._normalize_datetime(occurred_at)
        self._private_note = self._normalize_private_note(private_note)

    @classmethod
    def create(
        cls,
        owner_id: UserId,
        therapist_id: TherapistId,
        occurred_at: datetime,
        now: datetime,
        private_note: str | None = None,
    ) -> TherapySession:
        normalized_occurred_at = cls._normalize_datetime(occurred_at)
        normalized_now = cls._normalize_datetime(now)
        if normalized_occurred_at > normalized_now:
            raise InvalidTherapySessionTimeError()
        return cls(
            TherapySessionId.new(),
            owner_id,
            therapist_id,
            normalized_occurred_at,
            private_note,
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
        return cls(id, owner_id, therapist_id, occurred_at, private_note)

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

    @property
    def id(self) -> TherapySessionId:
        return self._id

    @property
    def owner_id(self) -> UserId:
        return self._owner_id

    @property
    def therapist_id(self) -> TherapistId:
        return self._therapist_id

    @property
    def occurred_at(self) -> datetime:
        return self._occurred_at

    @property
    def private_note(self) -> str | None:
        return self._private_note

    def update_private_note(self, note: str | None) -> None:
        self._private_note = self._normalize_private_note(note)

    def __repr__(self) -> str:
        return (
            "TherapySession("
            f"id={self.id!r}, owner_id={self.owner_id!r}, "
            f"therapist_id={self.therapist_id!r}, occurred_at={self.occurred_at!r}"
            ")"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TherapySession):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'TherapySession'")

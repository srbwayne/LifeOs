from datetime import datetime, timedelta, timezone

import pytest

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.aggregates.therapy_session import (
    PRIVATE_NOTE_MAX_LENGTH,
    TherapySession,
)
from app.therapy.domain.errors.therapy_errors import (
    InvalidPrivateNoteError,
    InvalidTherapySessionTimeError,
)
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId

NOW = datetime(2026, 9, 9, 12, 0, tzinfo=timezone.utc)
OCCURRED_AT = NOW - timedelta(days=1)


def create_session(**overrides: object) -> TherapySession:
    values: dict[str, object] = {
        "owner_id": UserId.new(),
        "therapist_id": TherapistId.new(),
        "occurred_at": OCCURRED_AT,
        "now": NOW,
    }
    values.update(overrides)
    return TherapySession.create(**values)  # type: ignore[arg-type]


def test_create_therapy_session_generates_id_and_preserves_domain_state() -> None:
    owner_id = UserId.new()
    therapist_id = TherapistId.new()

    session = create_session(owner_id=owner_id, therapist_id=therapist_id)

    assert isinstance(session.id, TherapySessionId)
    assert session.owner_id == owner_id
    assert session.therapist_id == therapist_id
    assert session.occurred_at == OCCURRED_AT
    assert session.domain_events == []


def test_non_utc_aware_occurred_at_is_normalized_to_utc() -> None:
    offset = timezone(timedelta(hours=-3))
    occurred_at = datetime(2026, 9, 9, 8, 0, tzinfo=offset)

    session = create_session(occurred_at=occurred_at)

    assert session.occurred_at == datetime(2026, 9, 9, 11, 0, tzinfo=timezone.utc)
    assert session.occurred_at.tzinfo is timezone.utc


def test_create_rejects_naive_occurred_at() -> None:
    with pytest.raises(InvalidTherapySessionTimeError):
        create_session(occurred_at=datetime(2026, 9, 9, 11, 0))


def test_create_rejects_future_occurred_at_using_injected_now() -> None:
    with pytest.raises(InvalidTherapySessionTimeError):
        create_session(occurred_at=NOW + timedelta(microseconds=1))


def test_create_accepts_current_occurred_at() -> None:
    assert create_session(occurred_at=NOW).occurred_at == NOW


@pytest.mark.parametrize("note", [None, "", "   "])
def test_private_note_absent_or_whitespace_normalizes_to_none(note: str | None) -> None:
    assert create_session(private_note=note).private_note is None


def test_private_note_is_trimmed_and_maximum_length_is_inclusive() -> None:
    note = "x" * PRIVATE_NOTE_MAX_LENGTH

    session = create_session(private_note=f"  {note}  ")

    assert session.private_note == note


def test_private_note_over_limit_is_rejected_without_echoing_body() -> None:
    secret = "private-body-" + ("x" * PRIVATE_NOTE_MAX_LENGTH)

    with pytest.raises(InvalidPrivateNoteError) as error:
        create_session(private_note=secret)

    assert secret not in str(error.value)


def test_private_note_update_and_clear_preserve_structural_state() -> None:
    session = create_session(private_note="Initial")
    structural = (session.id, session.owner_id, session.therapist_id, session.occurred_at)

    session.update_private_note("  Updated  ")
    assert session.private_note == "Updated"
    session.update_private_note("   ")

    assert session.private_note is None
    assert (session.id, session.owner_id, session.therapist_id, session.occurred_at) == structural


def test_restore_preserves_id_and_normalizes_persisted_values() -> None:
    identifier = TherapySessionId.new()
    occurred_at = datetime(2026, 9, 8, 9, 0, tzinfo=timezone(timedelta(hours=-3)))

    session = TherapySession.restore(
        id=identifier,
        owner_id=UserId.new(),
        therapist_id=TherapistId.new(),
        occurred_at=occurred_at,
        private_note="  Restored  ",
    )

    assert session.id == identifier
    assert session.occurred_at == datetime(2026, 9, 8, 12, 0, tzinfo=timezone.utc)
    assert session.private_note == "Restored"


@pytest.mark.parametrize("attribute", ["id", "owner_id", "therapist_id", "occurred_at"])
def test_therapy_session_structural_attributes_are_read_only(attribute: str) -> None:
    session = create_session()

    with pytest.raises(AttributeError):
        setattr(session, attribute, object())


def test_private_note_is_only_supported_business_mutation_and_repr_is_safe() -> None:
    secret = "private therapy reflection"
    session = create_session(private_note=secret)
    structural = (session.id, session.owner_id, session.therapist_id, session.occurred_at)

    session.update_private_note("Updated reflection")
    assert session.private_note == "Updated reflection"
    session.update_private_note(None)

    assert session.private_note is None
    assert (session.id, session.owner_id, session.therapist_id, session.occurred_at) == structural
    assert secret not in repr(session)
    assert session.domain_events == []

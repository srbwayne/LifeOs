from datetime import datetime, timezone

import pytest

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.commands.create_therapy_session import (
    CreateTherapySessionCommand,
    CreateTherapySessionCommandHandler,
)
from app.therapy.application.dtos.therapy_session_dto import (
    TherapySessionDetailDTO,
    TherapySessionHistoryItemDTO,
)
from app.therapy.application.errors import (
    InactiveTherapistError,
    TherapistNotFoundError,
    TherapySessionNotFoundError,
)
from app.therapy.application.queries.get_therapy_session import (
    GetTherapySessionQuery,
    GetTherapySessionQueryHandler,
)
from app.therapy.application.queries.list_therapy_sessions import (
    ListTherapySessionsQuery,
    ListTherapySessionsQueryHandler,
)
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.errors.therapy_errors import (
    InvalidPrivateNoteError,
    InvalidTherapySessionTimeError,
)
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId


class Repo:
    def __init__(self, therapist=None):
        self.therapist = therapist
        self.saved = []

    def get_by_id_and_owner(self, therapist_id, owner_id):
        return (
            self.therapist
            if self.therapist
            and self.therapist.id == therapist_id
            and self.therapist.owner_id == owner_id
            else None
        )

    def save(self, value):
        self.saved.append(value)


class Sessions:
    def __init__(self):
        self.saved = []

    def save(self, value):
        self.saved.append(value)

    def get_by_id_and_owner(self, *_):
        return None

    def delete(self, _):
        pass


class Uow:
    def __init__(self):
        self.commits = 0

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def commit(self):
        self.commits += 1

    def flush(self):
        pass

    def rollback(self):
        pass

    def track_aggregate(self, _):
        pass


def test_create_session_injects_clock_and_normalizes_note():
    owner = UserId.new()
    therapist = Therapist.create(owner, "Dr. A")
    sessions, uow = Sessions(), Uow()
    calls: list[int] = []

    def now_provider() -> datetime:
        calls.append(1)
        return datetime(2026, 1, 2, tzinfo=timezone.utc)

    result = CreateTherapySessionCommandHandler(
        Repo(therapist),
        sessions,
        uow,
        now_provider,
    )(
        CreateTherapySessionCommand(
            owner, therapist.id, datetime(2026, 1, 1, 21, tzinfo=timezone.utc), "  note  "
        )
    )
    assert result.therapist_name == "Dr. A" and result.private_note == "note"
    assert sessions.saved[0].owner_id == owner
    assert sessions.saved[0].therapist_id == therapist.id
    assert sessions.saved[0].occurred_at == datetime(2026, 1, 1, 21, tzinfo=timezone.utc)
    assert calls == [1]
    assert len(sessions.saved) == 1 and uow.commits == 1


def test_create_blank_note_is_none():
    owner = UserId.new()
    therapist = Therapist.create(owner, "Dr. A")
    sessions, uow = Sessions(), Uow()
    result = CreateTherapySessionCommandHandler(
        Repo(therapist), sessions, uow, lambda: datetime(2026, 1, 2, tzinfo=timezone.utc)
    )(
        CreateTherapySessionCommand(
            owner, therapist.id, datetime(2026, 1, 1, tzinfo=timezone.utc), "   "
        )
    )
    assert sessions.saved[0].private_note is None and result.private_note is None


def test_create_session_missing_or_inactive_therapist_does_not_commit():
    owner = UserId.new()
    sessions, uow = Sessions(), Uow()
    handler = CreateTherapySessionCommandHandler(
        Repo(), sessions, uow, lambda: datetime.now(timezone.utc)
    )
    with pytest.raises(TherapistNotFoundError):
        handler(CreateTherapySessionCommand(owner, TherapistId.new(), datetime.now(timezone.utc)))
    assert uow.commits == 0


def test_create_session_rejects_invalid_time_and_note_without_commit():
    owner = UserId.new()
    therapist = Therapist.create(owner, "Dr. A")
    for occurred_at, note, error in (
        (datetime(2026, 1, 1), None, InvalidTherapySessionTimeError),
        (datetime(2026, 1, 3, tzinfo=timezone.utc), None, InvalidTherapySessionTimeError),
        (datetime(2026, 1, 1, tzinfo=timezone.utc), "x" * 10_001, InvalidPrivateNoteError),
    ):
        sessions, uow = Sessions(), Uow()
        with pytest.raises(error):
            CreateTherapySessionCommandHandler(
                Repo(therapist), sessions, uow, lambda: datetime(2026, 1, 2, tzinfo=timezone.utc)
            )(CreateTherapySessionCommand(owner, therapist.id, occurred_at, note))
        assert not sessions.saved and uow.commits == 0
    therapist = Therapist.create(owner, "Inactive")
    therapist.deactivate()
    handler = CreateTherapySessionCommandHandler(
        Repo(therapist), sessions, uow, lambda: datetime.now(timezone.utc)
    )
    with pytest.raises(InactiveTherapistError):
        handler(CreateTherapySessionCommand(owner, therapist.id, datetime.now(timezone.utc)))
    assert uow.commits == 0


def test_list_sessions_calculates_pagination():
    class Read:
        def get_by_id_and_owner(self, *_):
            return None

        def count_by_owner(self, owner):
            return 5

        def list_page_by_owner(self, owner, offset, limit):
            assert offset == 2 and limit == 2
            return (TherapySessionHistoryItemDTO("s", "t", "Dr. A", datetime.now(timezone.utc)),)

    result = ListTherapySessionsQueryHandler(Read())(ListTherapySessionsQuery(UserId.new(), 2, 2))
    assert result.total_items == 5 and result.total_pages == 3
    assert not hasattr(result.items[0], "private_note")


def test_list_sessions_empty_history_has_zero_pages():
    class EmptyRead:
        def get_by_id_and_owner(self, *_):
            return None

        def count_by_owner(self, _):
            return 0

        def list_page_by_owner(self, *_):
            return ()

    result = ListTherapySessionsQueryHandler(EmptyRead())(
        ListTherapySessionsQuery(UserId.new(), 1, 20)
    )
    assert result.total_pages == 0 and result.items == ()


def test_get_session_owner_safe_detail_and_not_found():
    owner = UserId.new()
    session_id = TherapySessionId.new()
    detail = TherapySessionDetailDTO("s", "t", "Dr. A", datetime.now(timezone.utc), "note")

    class Read:
        def __init__(self, value):
            self.value = value

        def get_by_id_and_owner(self, *_):
            return self.value

        def count_by_owner(self, _):
            return 0

        def list_page_by_owner(self, *_):
            return ()

    assert (
        GetTherapySessionQueryHandler(Read(detail))(GetTherapySessionQuery(owner, session_id))
        == detail
    )
    for value in (None,):
        with pytest.raises(TherapySessionNotFoundError):
            GetTherapySessionQueryHandler(Read(value))(GetTherapySessionQuery(owner, session_id))

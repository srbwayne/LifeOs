from datetime import datetime, timezone

import pytest

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.commands.create_therapy_session import (
    CreateTherapySessionCommand,
    CreateTherapySessionCommandHandler,
)
from app.therapy.application.errors import (
    InactiveTherapistError,
    TherapistNotFoundError,
)
from app.therapy.application.queries.list_therapy_sessions import (
    ListTherapySessionsQuery,
    ListTherapySessionsQueryHandler,
)
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.value_objects.therapist_id import TherapistId


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
    result = CreateTherapySessionCommandHandler(
        Repo(therapist), sessions, uow, lambda: datetime(2026, 1, 2, tzinfo=timezone.utc)
    )(
        CreateTherapySessionCommand(
            owner, therapist.id, datetime(2026, 1, 1, 21, tzinfo=timezone.utc), "  note  "
        )
    )
    assert result.therapist_name == "Dr. A" and result.private_note == "note"
    assert len(sessions.saved) == 1 and uow.commits == 1


def test_create_session_missing_or_inactive_therapist_does_not_commit():
    owner = UserId.new()
    sessions, uow = Sessions(), Uow()
    handler = CreateTherapySessionCommandHandler(
        Repo(), sessions, uow, lambda: datetime.now(timezone.utc)
    )
    with pytest.raises(TherapistNotFoundError):
        handler(CreateTherapySessionCommand(owner, TherapistId.new(), datetime.now(timezone.utc)))
    assert uow.commits == 0
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
            return ()

    result = ListTherapySessionsQueryHandler(Read())(ListTherapySessionsQuery(UserId.new(), 2, 2))
    assert result.total_items == 5 and result.total_pages == 3

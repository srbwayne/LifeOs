from datetime import datetime, timezone

import pytest

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.commands.create_therapy_session import CreateTherapySessionCommand
from app.therapy.application.commands.delete_therapy_session import (
    DeleteTherapySessionCommand,
    DeleteTherapySessionCommandHandler,
)
from app.therapy.application.commands.update_private_note import (
    UpdatePrivateNoteCommand,
    UpdatePrivateNoteCommandHandler,
)
from app.therapy.application.dtos.therapy_session_dto import (
    TherapySessionDetailDTO,
    TherapySessionPrivateNoteDTO,
)
from app.therapy.application.errors import TherapySessionNotFoundError
from app.therapy.domain.aggregates.therapy_session import TherapySession
from app.therapy.domain.errors.therapy_errors import InvalidPrivateNoteError
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId
from app.therapy.presentation.api.fastapi.schemas import (
    CreateTherapySessionRequest,
    TherapySessionDetailResponse,
    TherapySessionPrivateNoteResponse,
    UpdatePrivateNoteRequest,
)


class Repo:
    def __init__(self, session=None):
        self.session = session
        self.saved = []
        self.deleted = []
        self.lookups = []

    def get_by_id_and_owner(self, session_id, owner_id):
        self.lookups.append((session_id, owner_id))
        if self.session and self.session.id == session_id and self.session.owner_id == owner_id:
            return self.session
        return None

    def save(self, session):
        self.saved.append(session)

    def delete(self, session):
        self.deleted.append(session)


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


def make_session(owner: UserId) -> TherapySession:
    return TherapySession.create(
        owner,
        TherapistId.new(),
        datetime(2026, 1, 1, tzinfo=timezone.utc),
        datetime(2026, 1, 2, tzinfo=timezone.utc),
        "original",
    )


def test_update_private_note_is_owner_scoped_and_minimized():
    owner = UserId.new()
    session = make_session(owner)
    repo, uow = Repo(session), Uow()
    result = UpdatePrivateNoteCommandHandler(repo, uow)(
        UpdatePrivateNoteCommand(owner, session.id, "  revised  ")
    )
    assert result == TherapySessionPrivateNoteDTO(session.id.value, "revised")
    assert session.private_note == "revised" and len(repo.saved) == 1 and uow.commits == 1
    assert repo.lookups == [(session.id, owner)]
    assert "revised" not in repr(result)
    assert "revised" not in repr(UpdatePrivateNoteCommand(owner, session.id, "revised"))
    assert "known-sensitive-value" not in repr(
        CreateTherapySessionCommand(
            owner, session.therapist_id, session.occurred_at, "known-sensitive-value"
        )
    )


@pytest.mark.parametrize("note", [None, "   "])
def test_update_private_note_clear_preserves_structure(note):
    owner = UserId.new()
    session = make_session(owner)
    before = (session.owner_id, session.therapist_id, session.occurred_at)
    repo, uow = Repo(session), Uow()
    result = UpdatePrivateNoteCommandHandler(repo, uow)(
        UpdatePrivateNoteCommand(owner, session.id, note)
    )
    assert session.private_note is None and result.private_note is None
    assert len(repo.saved) == 1 and uow.commits == 1
    assert (session.owner_id, session.therapist_id, session.occurred_at) == before


def test_update_private_note_foreign_owner_is_not_found():
    owner_a, owner_b = UserId.new(), UserId.new()
    session = make_session(owner_b)
    repo, uow = Repo(session), Uow()
    with pytest.raises(TherapySessionNotFoundError):
        UpdatePrivateNoteCommandHandler(repo, uow)(
            UpdatePrivateNoteCommand(owner_a, session.id, "x")
        )
    assert not repo.saved and uow.commits == 0


def test_update_private_note_failures_do_not_save_or_commit():
    owner = UserId.new()
    repo, uow = Repo(), Uow()
    with pytest.raises(TherapySessionNotFoundError):
        UpdatePrivateNoteCommandHandler(repo, uow)(
            UpdatePrivateNoteCommand(owner, TherapySessionId.new(), "x")
        )
    assert not repo.saved and uow.commits == 0
    session = make_session(owner)
    repo, uow = Repo(session), Uow()
    with pytest.raises(InvalidPrivateNoteError):
        UpdatePrivateNoteCommandHandler(repo, uow)(
            UpdatePrivateNoteCommand(owner, session.id, "x" * 10_001)
        )
    assert not repo.saved and uow.commits == 0 and session.private_note == "original"


def test_delete_private_session_is_owner_scoped_and_commits_once():
    owner = UserId.new()
    session = make_session(owner)
    repo, uow = Repo(session), Uow()
    assert (
        DeleteTherapySessionCommandHandler(repo, uow)(
            DeleteTherapySessionCommand(owner, session.id)
        )
        is None
    )
    assert repo.deleted == [session] and uow.commits == 1


def test_delete_missing_session_does_not_delete_or_commit():
    owner = UserId.new()
    repo, uow = Repo(), Uow()
    with pytest.raises(TherapySessionNotFoundError):
        DeleteTherapySessionCommandHandler(repo, uow)(
            DeleteTherapySessionCommand(owner, TherapySessionId.new())
        )
    assert not repo.deleted and uow.commits == 0


def test_delete_foreign_session_does_not_delete_or_commit():
    owner_a, owner_b = UserId.new(), UserId.new()
    repo, uow = Repo(make_session(owner_b)), Uow()
    with pytest.raises(TherapySessionNotFoundError):
        DeleteTherapySessionCommandHandler(repo, uow)(
            DeleteTherapySessionCommand(owner_a, repo.session.id)
        )
    assert not repo.deleted and uow.commits == 0


def test_sensitive_repr_matrix_excludes_note_but_serialization_preserves_it():
    sentinel = "known-sensitive-value"
    owner = UserId.new()
    session = make_session(owner)
    command = CreateTherapySessionCommand(
        owner, session.therapist_id, session.occurred_at, sentinel
    )
    update_command = UpdatePrivateNoteCommand(owner, session.id, sentinel)
    detail_dto = TherapySessionDetailDTO(
        session.id.value, session.therapist_id.value, "Dr", session.occurred_at, sentinel
    )
    objects = [
        session,
        detail_dto,
        command,
        update_command,
        TherapySessionPrivateNoteDTO(session.id.value, sentinel),
        CreateTherapySessionRequest(
            therapist_id=session.therapist_id.value,
            occurred_at=session.occurred_at,
            private_note=sentinel,
        ),
        UpdatePrivateNoteRequest(private_note=sentinel),
        TherapySessionDetailResponse(
            id=session.id.value,
            therapist_id=session.therapist_id.value,
            therapist_name="Dr",
            occurred_at=session.occurred_at,
            private_note=sentinel,
        ),
        TherapySessionPrivateNoteResponse(id=session.id.value, private_note=sentinel),
    ]
    assert all(sentinel not in repr(obj) for obj in objects)
    assert (
        TherapySessionPrivateNoteResponse(id="x", private_note=sentinel).model_dump()[
            "private_note"
        ]
        == sentinel
    )

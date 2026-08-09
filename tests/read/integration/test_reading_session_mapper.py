from datetime import datetime, timedelta, timezone

from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.domain.value_objects.total_pages import TotalPages
from app.read.infrastructure.persistence.mappers.reading_session_mapper import (
    ReadingSessionMapper,
)
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.shared.domain.identifiers.user_id import UserId

UTC_START = datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc)
UTC_END = datetime(2026, 8, 9, 12, 30, tzinfo=timezone.utc)


def make_session(notes: str | None = None) -> ReadingSession:
    return ReadingSession.create(
        owner_id=UserId.new(),
        book_id=BookId.new(),
        start_page=10,
        end_page=22,
        started_at=UTC_START,
        ended_at=UTC_END,
        book_total_pages=TotalPages(300),
        notes=notes,
    )


def test_mapper_converts_all_fields_without_persisting_pages_read() -> None:
    session = make_session("reflection")

    model = ReadingSessionMapper.to_persistence(session)

    assert model.id == session.id.to_persistence()
    assert model.user_id == session.owner_id.to_persistence()
    assert model.book_id == session.book_id.to_persistence()
    assert model.start_page == 10
    assert model.end_page == 22
    assert model.started_at == UTC_START
    assert model.ended_at == UTC_END
    assert model.notes == "reflection"
    assert not hasattr(model, "pages_read")


def test_mapper_round_trip_preserves_ids_pages_notes_and_events() -> None:
    session = make_session("reflection")

    restored = ReadingSessionMapper.to_domain(ReadingSessionMapper.to_persistence(session))

    assert restored.id == session.id
    assert restored.owner_id == session.owner_id
    assert restored.book_id == session.book_id
    assert restored.start_page == session.start_page
    assert restored.end_page == session.end_page
    assert restored.pages_read == 13
    assert restored.notes == "reflection"
    assert restored.domain_events == []


def test_mapper_preserves_absent_notes() -> None:
    restored = ReadingSessionMapper.to_domain(ReadingSessionMapper.to_persistence(make_session()))

    assert restored.notes is None


def test_mapper_interprets_sqlite_naive_datetimes_as_utc_without_new_id() -> None:
    session_id = ReadingSessionId.new()
    model = ReadingSessionModel(
        id=session_id.to_persistence(),
        user_id=UserId.new().to_persistence(),
        book_id=BookId.new().to_persistence(),
        start_page=1,
        end_page=1,
        started_at=UTC_START.replace(tzinfo=None),
        ended_at=UTC_END.replace(tzinfo=None),
        notes=None,
    )

    restored = ReadingSessionMapper.to_domain(model)

    assert restored.id == session_id
    assert restored.started_at == UTC_START
    assert restored.ended_at == UTC_END
    assert restored.started_at.tzinfo is timezone.utc
    assert restored.ended_at.tzinfo is timezone.utc


def test_mapper_normalizes_aware_offsets_to_utc() -> None:
    offset = timezone(timedelta(hours=-3))
    model = ReadingSessionMapper.to_persistence(make_session())
    model.started_at = datetime(2026, 8, 9, 9, 0, tzinfo=offset)
    model.ended_at = datetime(2026, 8, 9, 9, 30, tzinfo=offset)

    restored = ReadingSessionMapper.to_domain(model)

    assert restored.started_at == UTC_START
    assert restored.ended_at == UTC_END

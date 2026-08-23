from datetime import datetime, timedelta, timezone

from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.value_objects.book_completion_id import BookCompletionId
from app.read.domain.value_objects.book_id import BookId
from app.read.infrastructure.persistence.mappers.book_completion_mapper import (
    BookCompletionMapper,
)
from app.read.infrastructure.persistence.models.book_completion_model import (
    BookCompletionModel,
)

COMPLETED_AT = datetime(2026, 8, 22, 21, 0, tzinfo=timezone.utc)


def test_mapper_converts_completion_to_persistence_without_technical_fields() -> None:
    completion = BookCompletion.create(BookId.new(), COMPLETED_AT)

    model = BookCompletionMapper.to_persistence(completion)

    assert model.id == completion.id.to_persistence()
    assert model.book_id == completion.book_id.to_persistence()
    assert model.completed_at == COMPLETED_AT
    assert BookCompletionModel.__table__.c.get("owner_id") is None
    assert BookCompletionModel.__table__.c.get("user_id") is None
    assert BookCompletionModel.__table__.c.get("updated_at") is None


def test_mapper_restores_persisted_identity_and_utc_instant() -> None:
    completion_id = BookCompletionId.new()
    book_id = BookId.new()
    model = BookCompletionModel(
        id=completion_id.to_persistence(),
        book_id=book_id.to_persistence(),
        completed_at=COMPLETED_AT,
    )

    restored = BookCompletionMapper.to_domain(model)

    assert restored.id == completion_id
    assert restored.book_id == book_id
    assert restored.completed_at == COMPLETED_AT
    assert restored.completed_at.tzinfo is timezone.utc
    assert restored.domain_events == []


def test_mapper_interprets_sqlite_naive_datetime_as_utc() -> None:
    model = BookCompletionModel(
        id=BookCompletionId.new().to_persistence(),
        book_id=BookId.new().to_persistence(),
        completed_at=datetime(2026, 8, 22, 21, 0),
    )

    restored = BookCompletionMapper.to_domain(model)

    assert restored.completed_at == COMPLETED_AT
    assert restored.completed_at.tzinfo is timezone.utc


def test_mapper_normalizes_aware_non_utc_datetime_preserving_instant() -> None:
    model = BookCompletionModel(
        id=BookCompletionId.new().to_persistence(),
        book_id=BookId.new().to_persistence(),
        completed_at=datetime(2026, 8, 22, 18, 0, tzinfo=timezone(-timedelta(hours=3))),
    )

    restored = BookCompletionMapper.to_domain(model)

    assert restored.completed_at == COMPLETED_AT
    assert restored.completed_at.tzinfo is timezone.utc


def test_mapper_keeps_created_at_outside_domain_state() -> None:
    model = BookCompletionModel(
        id=BookCompletionId.new().to_persistence(),
        book_id=BookId.new().to_persistence(),
        completed_at=COMPLETED_AT,
        created_at=datetime(2026, 8, 22, 22, 0),
    )

    restored = BookCompletionMapper.to_domain(model)

    assert not hasattr(restored, "created_at")

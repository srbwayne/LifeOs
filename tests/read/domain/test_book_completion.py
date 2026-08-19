from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.errors.book_completion_errors import (
    InvalidBookCompletionTimeError,
)
from app.read.domain.value_objects.book_completion_id import BookCompletionId
from app.read.domain.value_objects.book_id import BookId

UTC_COMPLETED_AT = datetime(2026, 8, 18, 15, 30, tzinfo=timezone.utc)


def create_completion(**overrides: object) -> BookCompletion:
    values: dict[str, object] = {
        "book_id": BookId.new(),
        "completed_at": UTC_COMPLETED_AT,
    }
    values.update(overrides)
    return BookCompletion.create(**values)  # type: ignore[arg-type]


def restore_completion(**overrides: object) -> BookCompletion:
    values: dict[str, object] = {
        "id": BookCompletionId.new(),
        "book_id": BookId.new(),
        "completed_at": UTC_COMPLETED_AT,
    }
    values.update(overrides)
    return BookCompletion.restore(**values)  # type: ignore[arg-type]


def test_create_generates_id_and_preserves_book_and_completed_at() -> None:
    book_id = BookId.new()

    completion = create_completion(book_id=book_id)

    assert isinstance(completion.id, BookCompletionId)
    assert completion.book_id == book_id
    assert completion.completed_at == UTC_COMPLETED_AT
    assert completion.completed_at.tzinfo is timezone.utc


def test_restore_preserves_id_book_and_completed_at() -> None:
    completion_id = BookCompletionId.new()
    book_id = BookId.new()

    completion = restore_completion(id=completion_id, book_id=book_id)

    assert completion.id == completion_id
    assert completion.book_id == book_id
    assert completion.completed_at == UTC_COMPLETED_AT


@pytest.mark.parametrize("factory", [create_completion, restore_completion])
def test_offset_aware_completed_at_is_normalized_to_utc(factory: object) -> None:
    offset = timezone(timedelta(hours=-3))
    completed_at = datetime(2026, 8, 18, 12, 30, tzinfo=offset)

    completion = factory(completed_at=completed_at)  # type: ignore[operator]

    assert completion.completed_at == UTC_COMPLETED_AT
    assert completion.completed_at.tzinfo is timezone.utc


@pytest.mark.parametrize("factory", [create_completion, restore_completion])
def test_naive_completed_at_is_rejected(factory: object) -> None:
    with pytest.raises(InvalidBookCompletionTimeError):
        factory(completed_at=datetime(2026, 8, 18, 15, 30))  # type: ignore[operator]


@pytest.mark.parametrize("factory", [create_completion, restore_completion])
def test_non_datetime_completed_at_is_rejected(factory: object) -> None:
    with pytest.raises(InvalidBookCompletionTimeError):
        factory(completed_at="2026-08-18T15:30:00Z")  # type: ignore[operator]


@pytest.mark.parametrize("factory", [create_completion, restore_completion])
def test_invalid_book_id_type_is_rejected(factory: object) -> None:
    with pytest.raises(TypeError, match="book must be a BookId"):
        factory(book_id="book-id")  # type: ignore[operator]


def test_invalid_restored_id_type_is_rejected() -> None:
    with pytest.raises(TypeError, match="ID must be a BookCompletionId"):
        restore_completion(id="completion-id")


def test_direct_construction_cannot_bypass_invariants() -> None:
    with pytest.raises(TypeError, match="book must be a BookId"):
        BookCompletion(
            id=BookCompletionId.new(),
            book_id="book-id",  # type: ignore[arg-type]
            completed_at=UTC_COMPLETED_AT,
        )


def test_functional_state_contains_only_frozen_contract_fields() -> None:
    assert [field.name for field in fields(BookCompletion)] == [
        "id",
        "book_id",
        "completed_at",
    ]


@pytest.mark.parametrize("field", ["id", "book_id", "completed_at"])
def test_functional_state_cannot_be_reassigned(field: str) -> None:
    completion = create_completion()

    with pytest.raises(FrozenInstanceError):
        setattr(completion, field, object())


def test_equality_uses_only_identity() -> None:
    completion_id = BookCompletionId.new()
    first = restore_completion(id=completion_id)
    second = restore_completion(
        id=completion_id,
        book_id=BookId.new(),
        completed_at=UTC_COMPLETED_AT + timedelta(days=1),
    )

    assert first == second


def test_completions_with_different_ids_are_different() -> None:
    book_id = BookId.new()

    assert create_completion(book_id=book_id) != create_completion(book_id=book_id)


def test_book_completion_is_equal_only_to_another_completion() -> None:
    completion = create_completion()

    assert completion != completion.id


def test_book_completion_is_not_hashable() -> None:
    with pytest.raises(TypeError, match="unhashable type"):
        hash(create_completion())


def test_create_and_restore_do_not_produce_domain_events() -> None:
    assert create_completion().domain_events == []
    assert restore_completion().domain_events == []

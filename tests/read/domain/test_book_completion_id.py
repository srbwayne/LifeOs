import pytest
from tsidpy import TSID

from app.read.domain.value_objects.book_completion_id import BookCompletionId


def test_book_completion_id_generation_produces_valid_canonical_tsid() -> None:
    completion_id = BookCompletionId.new()

    assert completion_id.value
    assert TSID.from_string(completion_id.value).to_string() == completion_id.value
    assert BookCompletionId.from_value(completion_id.value) == completion_id


def test_book_completion_id_restoration_preserves_persistence_and_string() -> None:
    created = BookCompletionId.new()
    restored = BookCompletionId.from_value(created.to_persistence())

    assert restored == created
    assert hash(restored) == hash(created)
    assert str(restored) == created.value
    assert restored.to_persistence() == created.value


@pytest.mark.parametrize("value", ["", "not-a-tsid"])
def test_book_completion_id_rejects_empty_or_invalid_value(value: str) -> None:
    with pytest.raises(ValueError):
        BookCompletionId.from_value(value)


def test_book_completion_id_rejects_noncanonical_representation() -> None:
    canonical = BookCompletionId.new().value
    noncanonical = canonical.lower()

    if noncanonical == canonical:
        pytest.skip("Generated TSID contains no alphabetic characters.")

    with pytest.raises(ValueError):
        BookCompletionId.from_value(noncanonical)


@pytest.mark.parametrize("value", [None, 123, object()])
def test_book_completion_id_rejects_non_string_value(value: object) -> None:
    with pytest.raises(ValueError):
        BookCompletionId.from_value(value)  # type: ignore[arg-type]

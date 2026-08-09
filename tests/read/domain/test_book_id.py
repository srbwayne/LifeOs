import pytest

from app.read.domain.value_objects.book_id import BookId


def test_book_id_generation_produces_valid_canonical_tsid() -> None:
    book_id = BookId.new()

    assert book_id.value
    assert BookId.from_value(book_id.value) == book_id


def test_book_id_restoration_preserves_value_and_representation() -> None:
    created = BookId.new()
    restored = BookId.from_value(created.to_persistence())

    assert restored == created
    assert hash(restored) == hash(created)
    assert str(restored) == created.value
    assert restored.to_persistence() == created.value


@pytest.mark.parametrize("value", ["", "not-a-tsid"])
def test_book_id_rejects_empty_or_invalid_value(value: str) -> None:
    with pytest.raises(ValueError):
        BookId.from_value(value)


def test_book_id_rejects_noncanonical_representation() -> None:
    canonical = BookId.new().value
    noncanonical = canonical.lower()

    if noncanonical == canonical:
        pytest.skip("Generated TSID contains no alphabetic characters.")

    with pytest.raises(ValueError):
        BookId.from_value(noncanonical)

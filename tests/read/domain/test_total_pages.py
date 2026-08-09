import pytest

from app.read.domain.errors.book_errors import InvalidTotalPagesError
from app.read.domain.value_objects.total_pages import TotalPages


def test_total_pages_accepts_positive_integer() -> None:
    total_pages = TotalPages(320)

    assert total_pages.value == 320


@pytest.mark.parametrize("value", [0, -1, True, False, 1.5, "100", None])
def test_total_pages_rejects_non_positive_or_non_integer_value(value: object) -> None:
    with pytest.raises(InvalidTotalPagesError):
        TotalPages(value)  # type: ignore[arg-type]


def test_total_pages_has_value_equality_and_hash() -> None:
    first = TotalPages(200)
    second = TotalPages(200)

    assert first == second
    assert hash(first) == hash(second)

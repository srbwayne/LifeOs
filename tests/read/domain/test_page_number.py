import pytest

from app.read.domain.errors.reading_session_errors import InvalidPageNumberError
from app.read.domain.value_objects.page_number import PageNumber


@pytest.mark.parametrize("value", [1, 2, 500])
def test_page_number_accepts_positive_integer(value: int) -> None:
    assert PageNumber(value).value == value


@pytest.mark.parametrize("value", [0, -1, True, False, 1.5, "1", None])
def test_page_number_rejects_invalid_value(value: object) -> None:
    with pytest.raises(InvalidPageNumberError):
        PageNumber(value)  # type: ignore[arg-type]


def test_page_number_has_value_equality_and_hash() -> None:
    first = PageNumber(42)
    second = PageNumber(42)

    assert first == second
    assert hash(first) == hash(second)

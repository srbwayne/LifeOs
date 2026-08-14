from dataclasses import FrozenInstanceError

import pytest

from app.read.domain.models.page_interval import PageInterval


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_rejects_invalid_start_type(value: object) -> None:
    with pytest.raises(TypeError):
        PageInterval(value, 2)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [True, False, 2.0, "2", None])
def test_rejects_invalid_end_type(value: object) -> None:
    with pytest.raises(TypeError):
        PageInterval(1, value)  # type: ignore[arg-type]


def test_enforces_bounds_length_and_frozen_state() -> None:
    with pytest.raises(ValueError):
        PageInterval(0, 1)
    with pytest.raises(ValueError):
        PageInterval(2, 1)
    interval = PageInterval(3, 7)
    assert interval.length == 5
    with pytest.raises(FrozenInstanceError):
        interval.end_page = 8  # type: ignore[misc]

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from app.read.domain.models.reading_progress import ReadingProgress
from app.read.domain.value_objects.book_id import BookId


def test_reading_progress_is_an_immutable_identityless_result() -> None:
    progress = ReadingProgress(
        book_id=BookId.new(),
        total_pages=100,
        unique_pages_read=20,
        highest_page_reached=20,
        percentage=Decimal("20.00"),
        completed=False,
    )

    with pytest.raises(FrozenInstanceError):
        progress.unique_pages_read = 21  # type: ignore[misc]

    assert not hasattr(progress, "id")
    assert not hasattr(progress, "domain_events")

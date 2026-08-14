from dataclasses import FrozenInstanceError, fields

import pytest

from app.read.domain.models.page_interval import PageInterval
from app.read.domain.models.reading_insights import ReadingInsights
from app.read.domain.value_objects.book_id import BookId


def make_insights() -> ReadingInsights:
    return ReadingInsights(BookId.new(), 5, (PageInterval(6, 10),), False, False)


def test_is_immutable_identityless_and_has_exact_fields() -> None:
    insights = make_insights()
    assert [field.name for field in fields(insights)] == [
        "book_id",
        "remaining_pages",
        "gaps",
        "last_page_reached_with_gaps",
        "full_coverage_confirmed",
    ]
    assert not hasattr(insights, "id")
    assert not hasattr(insights, "domain_events")
    assert not hasattr(insights, "message")
    with pytest.raises(FrozenInstanceError):
        insights.remaining_pages = 0  # type: ignore[misc]


def test_validates_own_structure() -> None:
    with pytest.raises(TypeError):
        ReadingInsights("book", 1, (), False, False)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ReadingInsights(BookId.new(), True, (), False, False)
    with pytest.raises(ValueError):
        ReadingInsights(BookId.new(), -1, (), False, False)
    with pytest.raises(TypeError):
        ReadingInsights(BookId.new(), 1, [], False, False)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        ReadingInsights(BookId.new(), 1, (PageInterval(1, 1),), False, True)

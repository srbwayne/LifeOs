from app.read.domain.errors.book_completion_errors import (
    InvalidBookCompletionTimeError,
)
from app.shared.domain.errors import DomainError


def test_invalid_book_completion_time_error_follows_domain_error_convention() -> None:
    error = InvalidBookCompletionTimeError()

    assert isinstance(error, DomainError)
    assert str(error) == "Book completion time must be a timezone-aware datetime."

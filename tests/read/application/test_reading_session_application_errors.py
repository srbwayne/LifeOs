from app.read.application.errors.book_errors import BookNotFoundError
from app.shared.domain.errors import DomainError


def test_book_not_found_error_is_an_application_error_with_stable_message() -> None:
    assert BookNotFoundError.__module__.startswith("app.read.application.errors")
    assert isinstance(BookNotFoundError(), DomainError)
    assert str(BookNotFoundError()) == "Book not found."

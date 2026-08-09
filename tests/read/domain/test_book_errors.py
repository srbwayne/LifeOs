from app.read.domain.errors.book_errors import (
    InvalidBookAuthorError,
    InvalidBookTitleError,
    InvalidTotalPagesError,
)


def test_invalid_book_title_error_has_stable_message() -> None:
    assert str(InvalidBookTitleError()) == "Book title cannot be empty."


def test_invalid_book_author_error_has_stable_message() -> None:
    assert str(InvalidBookAuthorError()) == "Book author cannot be empty."


def test_invalid_total_pages_error_has_stable_message() -> None:
    assert str(InvalidTotalPagesError()) == "Book total pages must be a positive integer."

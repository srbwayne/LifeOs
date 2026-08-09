from app.read.domain.errors.reading_session_errors import (
    InvalidPageNumberError,
    InvalidReadingRangeError,
    InvalidReadingSessionTimeError,
    ReadingBeyondBookError,
)


def test_invalid_page_number_error_has_stable_message() -> None:
    assert str(InvalidPageNumberError()) == (
        "Reading session page number must be a positive integer."
    )


def test_invalid_reading_range_error_has_stable_message() -> None:
    assert str(InvalidReadingRangeError()) == (
        "Reading session end page cannot precede the start page."
    )


def test_reading_beyond_book_error_has_stable_message() -> None:
    assert str(ReadingBeyondBookError()) == (
        "Reading session end page cannot exceed the book total pages."
    )


def test_invalid_reading_session_time_error_has_stable_message() -> None:
    assert str(InvalidReadingSessionTimeError()) == (
        "Reading session times must be timezone-aware and end at or after the start."
    )

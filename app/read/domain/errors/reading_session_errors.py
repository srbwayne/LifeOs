from app.shared.domain.errors import DomainError


class InvalidPageNumberError(DomainError):
    @property
    def message(self) -> str:
        return "Reading session page number must be a positive integer."


class InvalidReadingRangeError(DomainError):
    @property
    def message(self) -> str:
        return "Reading session end page cannot precede the start page."


class ReadingBeyondBookError(DomainError):
    @property
    def message(self) -> str:
        return "Reading session end page cannot exceed the book total pages."


class InvalidReadingSessionTimeError(DomainError):
    @property
    def message(self) -> str:
        return "Reading session times must be timezone-aware and end at or after the start."

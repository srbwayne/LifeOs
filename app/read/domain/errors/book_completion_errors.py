from app.shared.domain.errors import DomainError


class InvalidBookCompletionTimeError(DomainError):
    @property
    def message(self) -> str:
        return "Book completion time must be a timezone-aware datetime."

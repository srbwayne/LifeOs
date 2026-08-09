from app.shared.domain.errors import DomainError


class InvalidBookTitleError(DomainError):
    @property
    def message(self) -> str:
        return "Book title cannot be empty."


class InvalidBookAuthorError(DomainError):
    @property
    def message(self) -> str:
        return "Book author cannot be empty."


class InvalidTotalPagesError(DomainError):
    @property
    def message(self) -> str:
        return "Book total pages must be a positive integer."

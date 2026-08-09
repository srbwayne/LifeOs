from app.shared.domain.errors import DomainError


class BookNotFoundError(DomainError):
    @property
    def message(self) -> str:
        return "Book not found."

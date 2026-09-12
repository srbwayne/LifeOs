from app.shared.domain.errors import DomainError


class InvalidHabitNameError(DomainError):
    @property
    def message(self) -> str:
        return "Habit name must be a non-blank string."

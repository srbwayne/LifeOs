from app.shared.domain.errors import DomainError


class HabitNotFoundError(DomainError):
    @property
    def message(self) -> str:
        return "Habit not found."


class HabitAlreadyExistsError(DomainError):
    @property
    def message(self) -> str:
        return "Habit already exists."


class InactiveHabitError(DomainError):
    @property
    def message(self) -> str:
        return "Cannot create a completion for an inactive Habit."


class HabitCompletionNotFoundError(DomainError):
    @property
    def message(self) -> str:
        return "Habit completion not found."

from app.shared.domain.errors import DomainError


class TherapySessionNotFoundError(DomainError):
    @property
    def message(self) -> str:
        return "Therapy session not found."


class InactiveTherapistError(DomainError):
    @property
    def message(self) -> str:
        return "Therapist is inactive."

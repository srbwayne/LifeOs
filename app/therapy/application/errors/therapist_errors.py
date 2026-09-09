from app.shared.domain.errors import DomainError


class TherapistNotFoundError(DomainError):
    @property
    def message(self) -> str:
        return "Therapist not found."

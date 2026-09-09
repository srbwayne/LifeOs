from app.shared.domain.errors import DomainError


class InvalidTherapistNameError(DomainError):
    @property
    def message(self) -> str:
        return "Therapist name must be a non-blank string of at most 150 characters."


class InvalidTherapySessionTimeError(DomainError):
    @property
    def message(self) -> str:
        return "Therapy session occurrence must be timezone-aware and not in the future."


class InvalidPrivateNoteError(DomainError):
    @property
    def message(self) -> str:
        return "Therapy private note must be a string of at most 10000 characters or None."

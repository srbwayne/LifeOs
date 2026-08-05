from app.shared.domain.errors import DomainError


class PlayerAlreadyHasCharacterError(DomainError):
    @property
    def message(self) -> str:
        return "Player already has a Character."


class UserAlreadyHasPlayerError(DomainError):
    @property
    def message(self) -> str:
        return "User already has a Player."


class CharacterNotFoundError(DomainError):
    @property
    def message(self) -> str:
        return "Character not found."

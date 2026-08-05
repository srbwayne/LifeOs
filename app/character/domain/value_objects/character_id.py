from dataclasses import dataclass

from app.shared.domain.value_object import ValueObject


@dataclass(frozen=True)
class CharacterId(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Character ID cannot be empty.")

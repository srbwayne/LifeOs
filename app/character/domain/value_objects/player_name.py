from dataclasses import dataclass

from app.shared.domain.value_object import ValueObject


@dataclass(frozen=True)
class PlayerName(ValueObject):
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise ValueError("Player name cannot be empty.")
        object.__setattr__(self, "value", normalized)

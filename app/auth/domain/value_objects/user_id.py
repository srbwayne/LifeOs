from dataclasses import dataclass
from app.shared.domain.value_object import ValueObject

@dataclass(frozen=True)
class UserId(ValueObject):
    value: str

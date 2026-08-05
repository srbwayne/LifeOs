from dataclasses import dataclass
from app.shared.domain.value_object import ValueObject

@dataclass(frozen=True)
class HashedPassword(ValueObject):
    value: str

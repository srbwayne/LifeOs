from __future__ import annotations

from dataclasses import dataclass

from tsidpy import TSID

from app.shared.domain.tsid import new_tsid
from app.shared.domain.value_object import ValueObject


@dataclass(frozen=True)
class BookId(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value:
            raise ValueError("Book ID must be a non-empty TSID string.")
        try:
            parsed = TSID.from_string(self.value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Book ID must be a valid TSID string.") from exc
        if parsed.to_string() != self.value:
            raise ValueError("Book ID must use the canonical TSID representation.")

    @classmethod
    def new(cls) -> BookId:
        return cls(new_tsid())

    @classmethod
    def from_value(cls, value: str) -> BookId:
        return cls(value)

    def to_persistence(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value

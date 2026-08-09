from dataclasses import dataclass

from app.read.domain.errors.book_errors import InvalidTotalPagesError
from app.shared.domain.value_object import ValueObject


@dataclass(frozen=True)
class TotalPages(ValueObject):
    value: int

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, int) or self.value <= 0:
            raise InvalidTotalPagesError()

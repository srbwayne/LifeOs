from dataclasses import dataclass

from app.read.domain.errors.reading_session_errors import InvalidPageNumberError
from app.shared.domain.value_object import ValueObject


@dataclass(frozen=True)
class PageNumber(ValueObject):
    value: int

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, int) or self.value < 1:
            raise InvalidPageNumberError()

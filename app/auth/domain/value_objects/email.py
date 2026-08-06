import re
from dataclasses import dataclass

from app.auth.domain.errors.user_errors import InvalidEmailError
from app.shared.domain.value_object import ValueObject


@dataclass(frozen=True)
class Email(ValueObject):
    value: str

    def __post_init__(self):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, self.value):
            raise InvalidEmailError()

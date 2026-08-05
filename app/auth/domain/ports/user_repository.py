from typing import Protocol, Optional
from app.auth.domain.aggregates.user import User
from app.auth.domain.value_objects.email import Email
from app.shared.domain.identifiers.user_id import UserId

class IUserRepository(Protocol):
    def save(self, user: User) -> None:
        ...

    def find_by_id(self, user_id: UserId) -> Optional[User]:
        ...

    def find_by_email(self, email: Email) -> Optional[User]:
        ...

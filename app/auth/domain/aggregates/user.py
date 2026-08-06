from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.auth.domain.events.user_registered import UserRegistered
from app.auth.domain.value_objects.email import Email
from app.auth.domain.value_objects.hashed_password import HashedPassword
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId


@dataclass
class User(AggregateRoot):
    id: UserId
    email: Email
    hashed_password: HashedPassword
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def register(email: Email, hashed_password: HashedPassword) -> User:
        user_id = UserId.new()
        now = datetime.now()
        user = User(
            id=user_id, email=email, hashed_password=hashed_password, created_at=now, updated_at=now
        )
        user._add_domain_event(UserRegistered(user_id=user.id, email=user.email))
        return user

    def change_password(self, hashed_password: HashedPassword) -> None:
        self.hashed_password = hashed_password
        self.updated_at = datetime.now()

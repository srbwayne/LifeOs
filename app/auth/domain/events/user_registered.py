from dataclasses import dataclass

from app.auth.domain.value_objects.email import Email
from app.shared.domain.domain_event import DomainEvent
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: UserId
    email: Email

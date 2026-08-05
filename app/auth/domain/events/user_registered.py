from dataclasses import dataclass
from app.shared.domain.domain_event import DomainEvent
from app.auth.domain.value_objects.user_id import UserId
from app.auth.domain.value_objects.email import Email

@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: UserId
    email: Email

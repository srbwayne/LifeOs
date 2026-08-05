from typing import Protocol
from app.auth.domain.aggregates.user import User
from app.shared.domain.aggregate import AggregateRoot

class ICharacterFactory(Protocol):
    def create_initial(self, user: User) -> tuple[AggregateRoot, ...]:
        ...

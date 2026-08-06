from typing import Protocol

from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId


class ICharacterFactory(Protocol):
    def create_initial(
        self,
        user_id: UserId,
        email: str,
    ) -> tuple[AggregateRoot, ...]: ...

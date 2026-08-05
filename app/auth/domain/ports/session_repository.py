from typing import Protocol, Optional
from app.auth.domain.aggregates.session import Session

class ISessionRepository(Protocol):
    def save(self, session: Session) -> None:
        ...

    def find_by_refresh_token_hash(self, refresh_token_hash: str) -> Optional[Session]:
        ...

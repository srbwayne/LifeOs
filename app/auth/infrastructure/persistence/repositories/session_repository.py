from typing import Optional
from sqlalchemy.orm import Session as DbSession
from app.auth.domain.aggregates.session import Session
from app.auth.domain.ports.session_repository import ISessionRepository
from app.auth.infrastructure.persistence.mappers.session_mapper import SessionMapper
from app.auth.infrastructure.persistence.models.session_model import SessionModel

class SqlAlchemySessionRepository(ISessionRepository):
    def __init__(self, session: DbSession):
        self._session = session

    def save(self, session: Session) -> None:
        session_model = SessionMapper.to_persistence(session)
        self._session.merge(session_model)

    def find_by_refresh_token_hash(self, refresh_token_hash: str) -> Optional[Session]:
        session_model = self._session.query(SessionModel).filter_by(refresh_token_hash=refresh_token_hash).first()
        return SessionMapper.to_domain(session_model) if session_model else None

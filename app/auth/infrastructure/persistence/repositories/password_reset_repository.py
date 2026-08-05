from typing import Optional
from sqlalchemy.orm import Session as DbSession
from app.auth.domain.aggregates.password_reset import PasswordResetToken
from app.auth.domain.ports.password_reset_repository import IPasswordResetTokenRepository
from app.auth.infrastructure.persistence.mappers.password_reset_mapper import PasswordResetTokenMapper
from app.auth.infrastructure.persistence.models.password_reset_model import PasswordResetTokenModel

class SqlAlchemyPasswordResetTokenRepository(IPasswordResetTokenRepository):
    def __init__(self, session: DbSession):
        self._session = session

    def save(self, token: PasswordResetToken) -> None:
        token_model = PasswordResetTokenMapper.to_persistence(token)
        self._session.merge(token_model)

    def find_by_token_hash(self, token_hash: str) -> Optional[PasswordResetToken]:
        token_model = self._session.get(PasswordResetTokenModel, token_hash)
        return PasswordResetTokenMapper.to_domain(token_model) if token_model else None

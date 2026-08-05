from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId
from app.auth.domain.errors.user_errors import InvalidPasswordResetTokenError
import secrets
import hashlib

@dataclass
class PasswordResetToken(AggregateRoot):
    token_hash: str
    user_id: UserId
    expires_at: datetime
    is_used: bool

    @staticmethod
    def create(user_id: UserId, expires_in_minutes: int = 15) -> tuple[PasswordResetToken, str]:
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
        
        token_aggregate = PasswordResetToken(
            token_hash=token_hash,
            user_id=user_id,
            expires_at=expires_at,
            is_used=False
        )
        return token_aggregate, token

    def use(self):
        if self.is_used or self.expires_at < datetime.now():
            raise InvalidPasswordResetTokenError()
        self.is_used = True

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.tsid import new_tsid
from app.shared.domain.identifiers.user_id import UserId
from app.auth.domain.errors.user_errors import InvalidSessionError

@dataclass
class Session(AggregateRoot):
    id: str
    user_id: UserId
    refresh_token_hash: str
    user_agent: str | None
    ip_address: str | None
    expires_at: datetime
    created_at: datetime
    last_used_at: datetime
    revoked_at: datetime | None

    @staticmethod
    def start(
        user_id: UserId,
        refresh_token_hash: str,
        expires_at: datetime,
        user_agent: str | None,
        ip_address: str | None,
    ) -> Session:
        now = datetime.now()
        return Session(
            id=new_tsid(),
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=expires_at,
            created_at=now,
            last_used_at=now,
            revoked_at=None,
        )

    def revoke(self):
        if not self.revoked_at:
            self.revoked_at = datetime.now()
            self.updated_at = self.revoked_at

    def refresh(self, new_refresh_token_hash: str, new_expires_at: datetime):
        if self.revoked_at or self.expires_at < datetime.now():
            raise InvalidSessionError()
        
        self.refresh_token_hash = new_refresh_token_hash
        self.expires_at = new_expires_at
        self.last_used_at = datetime.now()
        self.updated_at = self.last_used_at

from app.auth.domain.aggregates.session import Session
from app.auth.infrastructure.persistence.models.session_model import SessionModel
from app.shared.domain.identifiers.user_id import UserId


class SessionMapper:
    @staticmethod
    def to_domain(model: SessionModel) -> Session:
        return Session(
            id=model.id,
            user_id=UserId.from_value(model.user_id),
            refresh_token_hash=model.refresh_token_hash,
            user_agent=model.user_agent,
            ip_address=model.ip_address,
            expires_at=model.expires_at,
            created_at=model.created_at,
            last_used_at=model.last_used_at,
            revoked_at=model.revoked_at,
        )

    @staticmethod
    def to_persistence(entity: Session) -> SessionModel:
        return SessionModel(
            id=entity.id,
            user_id=entity.user_id.to_persistence(),
            refresh_token_hash=entity.refresh_token_hash,
            user_agent=entity.user_agent,
            ip_address=entity.ip_address,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
            last_used_at=entity.last_used_at,
            revoked_at=entity.revoked_at,
        )

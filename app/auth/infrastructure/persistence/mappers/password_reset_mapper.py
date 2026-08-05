from app.auth.domain.aggregates.password_reset import PasswordResetToken
from app.shared.domain.identifiers.user_id import UserId
from app.auth.infrastructure.persistence.models.password_reset_model import PasswordResetTokenModel

class PasswordResetTokenMapper:
    @staticmethod
    def to_domain(model: PasswordResetTokenModel) -> PasswordResetToken:
        return PasswordResetToken(
            token_hash=model.token_hash,
            user_id=UserId.from_value(model.user_id),
            expires_at=model.expires_at,
            is_used=model.is_used,
        )

    @staticmethod
    def to_persistence(entity: PasswordResetToken) -> PasswordResetTokenModel:
        return PasswordResetTokenModel(
            token_hash=entity.token_hash,
            user_id=entity.user_id.to_persistence(),
            expires_at=entity.expires_at,
            is_used=entity.is_used,
        )

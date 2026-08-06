from typing import Protocol

from app.auth.domain.aggregates.password_reset import PasswordResetToken


class IPasswordResetTokenRepository(Protocol):
    def save(self, token: PasswordResetToken) -> None: ...

    def find_by_token_hash(self, token_hash: str) -> PasswordResetToken | None: ...

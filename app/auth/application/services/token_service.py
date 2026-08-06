from datetime import datetime, timedelta, timezone

import jwt

from app.auth.application.dtos.token_dtos import TokenDTO
from app.auth.domain.errors.user_errors import InvalidSessionError
from app.shared.domain.identifiers.user_id import UserId
from app.shared.domain.tsid import new_tsid


class TokenService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self._secret_key = secret_key
        self._algorithm = algorithm

    def generate_tokens(self, user_id: UserId) -> TokenDTO:
        access_token = self._create_access_token(user_id)
        refresh_token = self._create_refresh_token(user_id)
        return TokenDTO(access_token=access_token, refresh_token=refresh_token)

    def _create_access_token(self, user_id: UserId) -> str:
        payload = {
            "sub": user_id.value,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            "iat": datetime.now(timezone.utc),
            "jti": new_tsid(),
            "type": "access",
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def _create_refresh_token(self, user_id: UserId) -> str:
        payload = {
            "sub": user_id.value,
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
            "iat": datetime.now(timezone.utc),
            "jti": new_tsid(),
            "type": "refresh",
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str, expected_type: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
        except jwt.PyJWTError as exc:
            raise InvalidSessionError() from exc
        if payload.get("type") != expected_type:
            raise InvalidSessionError()
        return payload

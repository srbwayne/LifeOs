from typing import Protocol

from app.auth.domain.value_objects.hashed_password import HashedPassword


class IPasswordHasher(Protocol):
    def hash(self, password: str) -> HashedPassword: ...

    def verify(self, password: str, hashed_password: HashedPassword) -> bool: ...

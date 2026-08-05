from typing import Protocol


class IPasswordResetNotifier(Protocol):
    def send(self, email: str, token: str) -> None:
        ...

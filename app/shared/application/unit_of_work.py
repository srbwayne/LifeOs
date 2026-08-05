from typing import Protocol

class IUnitOfWork(Protocol):
    def __enter__(self) -> "IUnitOfWork":
        ...

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

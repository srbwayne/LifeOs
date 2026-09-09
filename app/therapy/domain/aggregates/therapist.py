from __future__ import annotations

from dataclasses import dataclass

from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.value_objects.therapist_id import TherapistId


@dataclass(eq=False)
class Therapist(AggregateRoot):
    id: TherapistId
    owner_id: UserId
    name: str
    active: bool

    @classmethod
    def create(cls, owner_id: UserId, name: str) -> Therapist:
        return cls._build(
            id=TherapistId.new(),
            owner_id=owner_id,
            name=name,
            active=True,
        )

    @classmethod
    def restore(
        cls,
        id: TherapistId,
        owner_id: UserId,
        name: str,
        active: bool,
    ) -> Therapist:
        if not isinstance(id, TherapistId):
            raise TypeError("Therapist ID must be a TherapistId.")
        return cls._build(id=id, owner_id=owner_id, name=name, active=active)

    @classmethod
    def _build(
        cls,
        id: TherapistId,
        owner_id: UserId,
        name: str,
        active: bool,
    ) -> Therapist:
        if not isinstance(owner_id, UserId):
            raise TypeError("Therapist owner must be a UserId.")
        if not isinstance(active, bool):
            raise TypeError("Therapist active must be a bool.")
        return cls(
            id=id,
            owner_id=owner_id,
            name=cls._normalize_name(name),
            active=active,
        )

    @staticmethod
    def _normalize_name(value: str) -> str:
        from app.therapy.domain.errors.therapy_errors import InvalidTherapistNameError

        if not isinstance(value, str) or not (normalized := value.strip()):
            raise InvalidTherapistNameError()
        if len(normalized) > 150:
            raise InvalidTherapistNameError()
        return normalized

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Therapist):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'Therapist'")

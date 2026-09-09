from __future__ import annotations

from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.errors.therapy_errors import InvalidTherapistNameError
from app.therapy.domain.value_objects.therapist_id import TherapistId


class Therapist(AggregateRoot):
    """Owner-scoped reusable Therapist aggregate root."""

    def __init__(
        self,
        id: TherapistId,
        owner_id: UserId,
        name: str,
        active: bool,
    ) -> None:
        super().__init__()
        if not isinstance(id, TherapistId):
            raise TypeError("Therapist ID must be a TherapistId.")
        if not isinstance(owner_id, UserId):
            raise TypeError("Therapist owner must be a UserId.")
        if not isinstance(active, bool):
            raise TypeError("Therapist active must be a bool.")
        self._id = id
        self._owner_id = owner_id
        self._name = self._normalize_name(name)
        self._active = active

    @classmethod
    def create(cls, owner_id: UserId, name: str) -> Therapist:
        return cls(TherapistId.new(), owner_id, name, True)

    @classmethod
    def restore(
        cls,
        id: TherapistId,
        owner_id: UserId,
        name: str,
        active: bool,
    ) -> Therapist:
        return cls(id, owner_id, name, active)

    @staticmethod
    def _normalize_name(value: str) -> str:
        if not isinstance(value, str) or not (normalized := value.strip()):
            raise InvalidTherapistNameError()
        if len(normalized) > 150:
            raise InvalidTherapistNameError()
        return normalized

    @property
    def id(self) -> TherapistId:
        return self._id

    @property
    def owner_id(self) -> UserId:
        return self._owner_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def active(self) -> bool:
        return self._active

    def deactivate(self) -> None:
        self._active = False

    def activate(self) -> None:
        self._active = True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Therapist):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'Therapist'")

import pytest

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.errors.therapy_errors import InvalidTherapistNameError
from app.therapy.domain.value_objects.therapist_id import TherapistId


def test_create_therapist_trims_name_and_defaults_active() -> None:
    owner_id = UserId.new()

    therapist = Therapist.create(owner_id, "  Dr. Example  ")

    assert isinstance(therapist.id, TherapistId)
    assert therapist.owner_id == owner_id
    assert therapist.name == "Dr. Example"
    assert therapist.active is True


@pytest.mark.parametrize("name", ["", "   ", "x" * 151])
def test_create_therapist_rejects_invalid_name(name: str) -> None:
    with pytest.raises(InvalidTherapistNameError):
        Therapist.create(UserId.new(), name)


def test_therapist_activation_is_idempotent_and_preserves_identity() -> None:
    therapist = Therapist.create(UserId.new(), "Example")
    identifier = therapist.id
    owner_id = therapist.owner_id

    therapist.deactivate()
    therapist.deactivate()
    assert therapist.active is False

    therapist.activate()
    therapist.activate()
    assert therapist.active is True
    assert therapist.id == identifier
    assert therapist.owner_id == owner_id


def test_restore_preserves_id_and_state() -> None:
    identifier = TherapistId.new()
    owner_id = UserId.new()

    therapist = Therapist.restore(identifier, owner_id, "  Example  ", False)

    assert therapist.id == identifier
    assert therapist.owner_id == owner_id
    assert therapist.name == "Example"
    assert therapist.active is False


def test_therapist_has_no_domain_events_or_structural_mutator() -> None:
    therapist = Therapist.create(UserId.new(), "Example")

    assert therapist.domain_events == []
    assert not {"update", "change_owner", "change_name"}.intersection(dir(therapist))

import pytest

from app.shared.domain.identifiers.user_id import UserId


def test_user_id_creation_restoration_and_value_semantics() -> None:
    created = UserId.new()
    restored = UserId.from_value(created.to_persistence())

    assert restored == created
    assert hash(restored) == hash(created)
    assert str(restored) == created.value
    assert restored.to_persistence() == created.value


@pytest.mark.parametrize('value', ['', 'user-1', '0r7azmtwhc2cv'])
def test_user_id_rejects_invalid_or_noncanonical_values(value: str) -> None:
    with pytest.raises(ValueError):
        UserId(value)

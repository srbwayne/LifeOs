from app.auth.domain.aggregates.user import User
from app.auth.domain.events.user_registered import UserRegistered
from app.auth.domain.value_objects.email import Email
from app.auth.domain.value_objects.hashed_password import HashedPassword


def test_user_registration_creates_user_and_raises_event():
    email = Email("test@example.com")
    hashed_password = HashedPassword("hashed_password_string")

    user = User.register(email=email, hashed_password=hashed_password)

    assert user.email == email
    assert user.hashed_password == hashed_password
    assert len(user.domain_events) == 1

    event = user.domain_events[0]
    assert isinstance(event, UserRegistered)
    assert event.user_id == user.id
    assert event.email == user.email

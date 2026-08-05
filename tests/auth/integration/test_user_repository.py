import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.shared.infrastructure.database import Base
from app.auth.domain.aggregates.user import User
from app.auth.domain.value_objects.email import Email
from app.auth.domain.value_objects.hashed_password import HashedPassword
from app.auth.infrastructure.persistence.repositories.user_repository import SqlAlchemyUserRepository

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(engine)

def test_can_save_and_retrieve_user(session):
    repository = SqlAlchemyUserRepository(session)
    email = Email("test@example.com")
    hashed_password = HashedPassword("hashed_password")
    user = User.register(email=email, hashed_password=hashed_password)

    repository.save(user)
    session.commit()

    retrieved_user = repository.find_by_id(user.id)

    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.email == user.email

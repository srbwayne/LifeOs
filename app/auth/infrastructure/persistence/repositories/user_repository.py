from typing import Optional
from sqlalchemy.orm import Session
from app.auth.domain.aggregates.user import User
from app.auth.domain.ports.user_repository import IUserRepository
from app.auth.domain.value_objects.email import Email
from app.shared.domain.identifiers.user_id import UserId
from app.auth.infrastructure.persistence.mappers.user_mapper import UserMapper
from app.auth.infrastructure.persistence.models.user_model import UserModel

class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, user: User) -> None:
        user_model = UserMapper.to_persistence(user)
        self._session.merge(user_model)

    def find_by_id(self, user_id: UserId) -> Optional[User]:
        user_model = self._session.get(UserModel, user_id.to_persistence())
        return UserMapper.to_domain(user_model) if user_model else None

    def find_by_email(self, email: Email) -> Optional[User]:
        user_model = self._session.query(UserModel).filter_by(email=email.value).first()
        return UserMapper.to_domain(user_model) if user_model else None

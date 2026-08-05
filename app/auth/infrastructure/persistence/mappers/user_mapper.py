from app.auth.domain.aggregates.user import User
from app.auth.domain.value_objects.email import Email
from app.auth.domain.value_objects.hashed_password import HashedPassword
from app.auth.domain.value_objects.user_id import UserId
from app.auth.infrastructure.persistence.models.user_model import UserModel

class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=UserId(model.id),
            email=Email(model.email),
            hashed_password=HashedPassword(model.hashed_password),
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_persistence(entity: User) -> UserModel:
        return UserModel(
            id=entity.id.value,
            email=entity.email.value,
            hashed_password=entity.hashed_password.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

from app.shared.domain.errors import DomainError

class UserAlreadyExistsError(DomainError):
    @property
    def message(self) -> str:
        return "User with this email already exists."

class InvalidEmailError(DomainError):
    @property
    def message(self) -> str:
        return "The provided email is not a valid email address."

class InvalidCredentialsError(DomainError):
    @property
    def message(self) -> str:
        return "Invalid email or password."

class InvalidSessionError(DomainError):
    @property
    def message(self) -> str:
        return "The authentication session is invalid or expired."

class InvalidPasswordResetTokenError(DomainError):
    @property
    def message(self) -> str:
        return "The password reset token is invalid or expired."

class UserNotFoundError(DomainError):
    @property
    def message(self) -> str:
        return "User not found."

from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.auth.domain.errors.user_errors import (
    InvalidCredentialsError,
    InvalidEmailError,
    InvalidPasswordResetTokenError,
    InvalidSessionError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.auth.presentation.api.fastapi.routers import router as auth_router
from app.character.domain.errors.character_errors import CharacterNotFoundError
from app.character.presentation.api.fastapi.routers import router as character_router
from app.read.domain.errors.book_errors import (
    InvalidBookAuthorError,
    InvalidBookTitleError,
    InvalidTotalPagesError,
)
from app.read.presentation.api.fastapi.routers import router as read_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Define o ciclo de vida da aplicação."""
    print("Inicializando a aplicação...")
    # Cria as tabelas no banco (para desenvolvimento local)
    yield
    print("Finalizando a aplicação...")


def create_app() -> FastAPI:
    """Cria e configura a instância da aplicação FastAPI."""
    app = FastAPI(title="LifeOS", lifespan=lifespan, docs_url="/docs", redoc_url="/redoc")

    # Inclui os roteadores das capabilities
    app.include_router(auth_router)
    app.include_router(character_router)
    app.include_router(read_router)

    error_statuses = {
        UserAlreadyExistsError: status.HTTP_409_CONFLICT,
        InvalidEmailError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
        InvalidSessionError: status.HTTP_401_UNAUTHORIZED,
        InvalidPasswordResetTokenError: status.HTTP_400_BAD_REQUEST,
        UserNotFoundError: status.HTTP_404_NOT_FOUND,
        CharacterNotFoundError: status.HTTP_404_NOT_FOUND,
        InvalidBookTitleError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        InvalidBookAuthorError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        InvalidTotalPagesError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    }
    for error_type, status_code in error_statuses.items():
        app.add_exception_handler(
            error_type,
            lambda _, exc, code=status_code: JSONResponse(
                status_code=code,
                content={"detail": str(exc)},
            ),
        )

    @app.get("/")
    def read_root():
        return {"message": "Welcome to LifeOS"}

    return app

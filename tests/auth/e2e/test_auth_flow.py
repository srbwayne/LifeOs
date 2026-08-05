import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.app_factory import create_app
from app.shared.infrastructure.database import Base
from app.auth.dependencies import get_db, get_password_reset_notifier

# --- Configuração do Banco de Dados de Teste ---
DATABASE_URL_TEST = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class FakePasswordResetNotifier:
    def __init__(self):
        self.tokens = []

    def send(self, email: str, token: str) -> None:
        self.tokens.append((email, token))


fake_notifier = FakePasswordResetNotifier()

# --- Sobrescrever a dependência get_db para usar o banco de teste ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# --- Fixture do Teste ---
@pytest.fixture(scope="function")
def client():
    # Cria uma nova instância do app para cada teste
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_password_reset_notifier] = lambda: fake_notifier
    fake_notifier.tokens.clear()
    
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


# --- Testes E2E ---
def test_full_auth_flow(client: TestClient):
    # 1. Registro
    response = client.post(
        "/auth/register",
        json={"email": "e2e@example.com", "password": "a_strong_password"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully."}

    # 2. Login
    response = client.post(
        "/auth/login",
        json={"email": "e2e@example.com", "password": "a_strong_password"},
    )
    assert response.status_code == 200
    login_data = response.json()
    assert "access_token" in login_data
    assert "refresh_token" in login_data

    # 3. Refresh token
    response = client.post("/auth/refresh")
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

    # 4. Logout
    response = client.post("/auth/logout")
    assert response.status_code == 204
    response = client.post("/auth/refresh")
    assert response.status_code == 401

    # 5. Solicitar redefinicao de senha
    response = client.post(
        "/auth/request-password-reset",
        json={"email": "e2e@example.com"},
    )
    assert response.status_code == 202
    assert fake_notifier.tokens[0][0] == "e2e@example.com"
    reset_token = fake_notifier.tokens[0][1]

    # 6. Redefinir senha
    response = client.post(
        "/auth/reset-password",
        json={"token": reset_token, "new_password": "a_new_strong_password"},
    )
    assert response.status_code == 204
    response = client.post(
        "/auth/reset-password",
        json={"token": reset_token, "new_password": "another_password"},
    )
    assert response.status_code == 400

    # 7. Autenticar com a nova senha
    response = client.post(
        "/auth/login",
        json={"email": "e2e@example.com", "password": "a_strong_password"},
    )
    assert response.status_code == 401
    response = client.post(
        "/auth/login",
        json={"email": "e2e@example.com", "password": "a_new_strong_password"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

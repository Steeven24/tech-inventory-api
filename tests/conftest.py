import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker


ROOT_DIR = Path(__file__).resolve().parent.parent
TEST_DB_PATH = ROOT_DIR / "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"

from core.database import Base, engine, get_db  # noqa: E402
from main import app  # noqa: E402
from models.user_model import User  # noqa: E402
from services.user_service import pwd_context  # noqa: E402

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
API_PREFIX = "/api/v1"


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    user = User(
        name="Admin User",
        email="admin@test.com",
        password=pwd_context.hash("Admin123!"),
        role="admin",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def seller_user(db_session):
    user = User(
        name="Seller User",
        email="seller@test.com",
        password=pwd_context.hash("Seller123!"),
        role="seller",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post(
        f"{API_PREFIX}/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

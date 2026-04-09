import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.task import Task
from app.utils.password import hash_password
from app.utils.rate_limiter import limiter
import functools

# Create engine with StaticPool for in-memory SQLite
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create all tables
Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

# Override the rate limiter for testing
def mock_limit(limit_string):
    """Mock limiter that just returns the function without modification."""
    def decorator(func):
        return func
    return decorator

limiter.limit = mock_limit

@pytest.fixture(autouse=True)
def clear_db():
    """Clear all data between tests."""
    yield
    # Clear all tables
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())

@pytest.fixture(scope="function")
def db() -> Session:
    """Get test database session."""
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def client():
    """Get test client."""
    return TestClient(app)

@pytest.fixture(scope="function")
def test_user(db: Session) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("TestPassword123"),
        is_active=True,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def admin_user(db: Session) -> User:
    """Create a test admin user."""
    admin = User(
        email="admin@example.com",
        hashed_password=hash_password("AdminPassword123"),
        is_active=True,
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture(scope="function")
def test_task(test_user: User, db: Session) -> Task:
    """Create a test task."""
    task = Task(
        title="Test Task",
        description="This is a test task",
        owner_id=test_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user: User):
    """Get authentication headers for test user."""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123"}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

@pytest.fixture(scope="function")
def admin_auth_headers(client: TestClient, admin_user: User):
    """Get authentication headers for admin user."""
    response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "AdminPassword123"}
    )
    assert response.status_code == 200, f"Admin login failed: {response.text}"
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database_new import Base, get_db
from ..models import User, Client, Opportunity, Task, Invoice, Points, Achievement, UserAchievement, Notification
from ..auth import create_access_token
from fastapi.testclient import TestClient
from ..main import app

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database session."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User(
        name="Test User",
        email="test@example.com",
        hashed_password="hashedpassword",
        role="user",
        company_id=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_client_data(db, test_user):
    """Create test client data."""
    client = Client(
        name="Test Client",
        email="client@example.com",
        phone="1234567890",
        company_id=test_user.company_id,
        created_by=test_user.id
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers."""
    token = create_access_token({"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}

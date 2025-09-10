import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from ..database_new import Base, get_db
from ..models import User
from ..auth import create_access_token
from ..main import app
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Test database setup
from sqlalchemy import create_engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_basic.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
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
    user = User(
        name="Test User",
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        company_id=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    token = create_access_token({"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}

def test_basic_setup(client):
    """Test that basic test setup works"""
    response = client.get("/")
    # Just check that we get some response (may be 404 for root, but app is working)
    assert response.status_code in [200, 404, 422]  # Any of these indicate the app is running

def test_database_connection(db):
    """Test that database connection works"""
    # Try to query users table
    users = db.query(User).all()
    assert isinstance(users, list)  # Should return a list even if empty

def test_user_creation(db):
    """Test that we can create a user in test database"""
    user = User(
        name="Test User",
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        company_id=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.name == "Test User"
    assert user.email == "test@example.com"

def test_auth_token_creation(test_user):
    """Test that auth token creation works"""
    token = create_access_token({"sub": test_user.email})
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

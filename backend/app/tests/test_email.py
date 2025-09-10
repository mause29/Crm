import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from ..database_new import Base, get_db
from ..models import User, Client
from ..auth import create_access_token
from ..main import app
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Test database setup
from sqlalchemy import create_engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_email.db"
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

@pytest.fixture
def test_clients(db, test_user):
    clients = [
        Client(
            name="Client One",
            email="client1@example.com",
            phone="1234567890",
            company_id=test_user.company_id,
            created_by=test_user.id
        ),
        Client(
            name="Client Two",
            email="client2@example.com",
            phone="0987654321",
            company_id=test_user.company_id,
            created_by=test_user.id
        ),
        Client(
            name="Client Three",
            email=None,  # No email for testing
            phone="5555555555",
            company_id=test_user.company_id,
            created_by=test_user.id
        )
    ]
    for client in clients:
        db.add(client)
    db.commit()
    return clients

@patch('backend.app.routes.email.send_email_background')
def test_send_single_email(mock_send_email, client, auth_headers):
    """Test sending a single email"""
    response = client.post(
        "/email/send",
        json={
            "to_email": "recipient@example.com",
            "subject": "Test Subject",
            "body": "Test body content"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "Email queued for sending" in response.json()["message"]

    # Verify the background task was called
    mock_send_email.assert_called_once_with(
        "recipient@example.com",
        "Test Subject",
        "Test body content"
    )

@patch('backend.app.routes.email.send_email_background')
def test_send_bulk_email(mock_send_email, client, auth_headers, test_clients, db):
    """Test sending bulk emails to multiple clients"""
    # Get client IDs (only those with emails)
    client_ids = [c.id for c in test_clients if c.email]

    response = client.post(
        "/email/send-bulk",
        json={
            "client_ids": client_ids,
            "subject": "Bulk Test Subject",
            "body": "Hello {{client_name}}, this is a test email."
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "Emails queued for 2 clients" in response.json()["message"]

    # Verify the background task was called for each client with email
    assert mock_send_email.call_count == 2

    # Check that the client name was replaced in the body
    calls = mock_send_email.call_args_list
    assert "Hello Client One," in calls[0][0][2]
    assert "Hello Client Two," in calls[1][0][2]

def test_get_email_templates(client, auth_headers):
    """Test getting email templates"""
    response = client.get("/email/templates", headers=auth_headers)
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) == 3
    assert templates[0]["name"] == "Welcome Email"
    assert templates[1]["name"] == "Follow-up Email"
    assert templates[2]["name"] == "Proposal Email"

def test_get_email_templates_by_category(client, auth_headers):
    """Test filtering email templates by category"""
    response = client.get("/email/templates?category=welcome", headers=auth_headers)
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) == 1
    assert templates[0]["category"] == "welcome"

def test_get_clients_for_email(client, auth_headers, test_clients):
    """Test getting clients with email addresses for bulk emailing"""
    response = client.get("/email/clients", headers=auth_headers)
    assert response.status_code == 200
    clients = response.json()

    # Should only return clients with email addresses
    assert len(clients) == 2
    emails = [c["email"] for c in clients]
    assert "client1@example.com" in emails
    assert "client2@example.com" in emails
    assert "client3@example.com" not in emails  # No email

def test_get_email_history(client, auth_headers):
    """Test getting email sending history"""
    response = client.get("/email/history", headers=auth_headers)
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 2  # Mock data returns 2 entries
    assert history[0]["status"] == "sent"
    assert "subject" in history[0]

def test_send_email_background_function():
    """Test the background email sending function"""
    from backend.app.routes.email import send_email_background

    # Mock SMTP server
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the function
        send_email_background(
            "test@example.com",
            "Test Subject",
            "Test body content"
        )

        # Verify SMTP calls
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

def test_send_email_background_error_handling():
    """Test error handling in background email sending"""
    from backend.app.routes.email import send_email_background

    # Mock SMTP to raise an exception
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_server.sendmail.side_effect = Exception("SMTP Error")
        mock_smtp.return_value = mock_server

        # This should not raise an exception, just log it
        send_email_background(
            "test@example.com",
            "Test Subject",
            "Test body content"
        )

        # Verify the function completed without raising
        mock_server.sendmail.assert_called_once()

@patch('backend.app.routes.email.SMTP_USERNAME', 'test@example.com')
@patch('backend.app.routes.email.SMTP_PASSWORD', 'testpassword')
def test_email_configuration(mock_password, mock_username, client, auth_headers):
    """Test email configuration from environment variables"""
    from backend.app.routes.email import SMTP_SERVER, SMTP_PORT

    # Verify default values
    assert SMTP_SERVER == "smtp.gmail.com"
    assert SMTP_PORT == 587

    # Test with mocked environment variables
    with patch.dict('os.environ', {
        'SMTP_SERVER': 'smtp.custom.com',
        'SMTP_PORT': '465',
        'SMTP_USERNAME': 'custom@example.com',
        'SMTP_PASSWORD': 'custompass'
    }):
        # Re-import to get new values
        import importlib
        import backend.app.routes.email
        importlib.reload(backend.app.routes.email)

        assert backend.app.routes.email.SMTP_SERVER == "smtp.custom.com"
        assert backend.app.routes.email.SMTP_PORT == 465

def test_email_template_structure(client, auth_headers):
    """Test that email templates have the correct structure"""
    response = client.get("/email/templates", headers=auth_headers)
    assert response.status_code == 200
    templates = response.json()

    for template in templates:
        assert "id" in template
        assert "name" in template
        assert "subject" in template
        assert "body" in template
        assert "category" in template
        assert isinstance(template["body"], str)
        assert len(template["body"]) > 0

def test_bulk_email_with_no_clients(client, auth_headers):
    """Test sending bulk email with empty client list"""
    response = client.post(
        "/email/send-bulk",
        json={
            "client_ids": [],
            "subject": "Test Subject",
            "body": "Test body"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "Emails queued for 0 clients" in response.json()["message"]

def test_bulk_email_with_invalid_client_ids(client, auth_headers):
    """Test sending bulk email with non-existent client IDs"""
    response = client.post(
        "/email/send-bulk",
        json={
            "client_ids": [999, 1000],  # Non-existent IDs
            "subject": "Test Subject",
            "body": "Test body"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "Emails queued for 0 clients" in response.json()["message"]

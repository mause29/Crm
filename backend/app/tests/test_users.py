import pytest
from passlib.context import CryptContext
from ..models import User

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "Password123!",
            "role": "user",
            "company_id": 1
        }
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "User created successfully"
    assert "user_id" in response.json()

def test_create_user_duplicate_email(client):
    # First create a user
    client.post(
        "/users/",
        json={
            "name": "First User",
            "email": "duplicate@example.com",
            "password": "Password123!",
            "role": "user",
            "company_id": 1
        }
    )

    # Try to create another user with the same email
    response = client.post(
        "/users/",
        json={
            "name": "Second User",
            "email": "duplicate@example.com",
            "password": "Password123!",
            "role": "user",
            "company_id": 1
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_create_user_invalid_password(client):
    response = client.post(
        "/users/",
        json={
            "name": "Invalid Password User",
            "email": "invalid@example.com",
            "password": "weak",
            "role": "user",
            "company_id": 1
        }
    )
    assert response.status_code == 422  # Validation error

def test_login_success(client, db):
    # Create a test user with known password
    hashed_password = get_password_hash("TestPassword123!")
    test_user = User(
        name="Login Test User",
        email="login@example.com",
        hashed_password=hashed_password,
        role="user",
        company_id=1,
        is_active=True
    )
    db.add(test_user)
    db.commit()

    response = client.post(
        "/users/token",
        data={"username": "login@example.com", "password": "TestPassword123!"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/users/token",
        data={"username": "nonexistent@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_login_inactive_user(client, db):
    # Create an inactive user
    hashed_password = get_password_hash("TestPassword123!")
    inactive_user = User(
        name="Inactive User",
        email="inactive@example.com",
        hashed_password=hashed_password,
        role="user",
        company_id=1,
        is_active=False
    )
    db.add(inactive_user)
    db.commit()

    response = client.post(
        "/users/token",
        data={"username": "inactive@example.com", "password": "TestPassword123!"}
    )
    assert response.status_code == 401
    assert "Account is deactivated" in response.json()["detail"]

def test_get_users_admin(client, auth_headers, db):
    # Create admin user for auth_headers
    admin_user = User(
        name="Admin User",
        email="admin@example.com",
        hashed_password=get_password_hash("AdminPass123!"),
        role="admin",
        company_id=1,
        is_active=True
    )
    db.add(admin_user)
    db.commit()

    # Override auth_headers to use admin token
    from ..auth import create_access_token
    admin_token = create_access_token({"sub": admin_user.email})
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.get("/users/", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_users_non_admin(client, auth_headers):
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 403
    assert "Admin access required" in response.json()["detail"]

def test_get_user_by_id(client, auth_headers, test_user):
    response = client.get(f"/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email

def test_get_user_not_found(client, auth_headers):
    response = client.get("/users/99999", headers=auth_headers)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_get_user_unauthorized(client, auth_headers, db):
    # Create another user
    other_user = User(
        name="Other User",
        email="other@example.com",
        hashed_password=get_password_hash("OtherPass123!"),
        role="user",
        company_id=1,
        is_active=True
    )
    db.add(other_user)
    db.commit()

    # Try to access other user's data with regular user auth
    response = client.get(f"/users/{other_user.id}", headers=auth_headers)
    assert response.status_code == 403
    assert "Not authorized to view this user" in response.json()["detail"]

def test_enable_2fa(client, auth_headers, test_user, db):
    response = client.post(f"/users/enable-2fa/{test_user.id}", headers=auth_headers, json={})
    assert response.status_code == 200
    assert "secret" in response.json()
    assert "uri" in response.json()

def test_enable_2fa_already_enabled(client, auth_headers, test_user, db):
    # First enable 2FA
    client.post(f"/users/enable-2fa/{test_user.id}", headers=auth_headers, json={})

    # Try to enable again using the same user ID
    response = client.post(f"/users/enable-2fa/{test_user.id}", headers=auth_headers, json={})
    assert response.status_code == 400
    assert "2FA already enabled" in response.json()["detail"]

def test_enable_2fa_unauthorized(client, auth_headers, db):
    # Create another user
    other_user = User(
        name="Other User",
        email="other2@example.com",
        hashed_password=get_password_hash("OtherPass123!"),
        role="user",
        company_id=1,
        is_active=True
    )
    db.add(other_user)
    db.commit()

    # Try to enable 2FA for other user
    response = client.post(f"/users/enable-2fa/{other_user.id}", headers=auth_headers, json={})
    assert response.status_code == 403
    assert "Not authorized to enable 2FA" in response.json()["detail"]

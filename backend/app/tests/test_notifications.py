import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from ..database_new import Base, get_db
from ..models import User, Notification, Task, Opportunity, Client
from ..auth import create_access_token
from ..main import app
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Test database setup
from sqlalchemy import create_engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_notifications.db"
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
def test_notifications(db, test_user):
    notifications = [
        Notification(
            title="Test Notification 1",
            message="This is test notification 1",
            type="info",
            user_id=test_user.id,
            is_read=False
        ),
        Notification(
            title="Test Notification 2",
            message="This is test notification 2",
            type="warning",
            user_id=test_user.id,
            is_read=True
        ),
        Notification(
            title="Test Notification 3",
            message="This is test notification 3",
            type="success",
            user_id=test_user.id,
            is_read=False
        )
    ]
    for notification in notifications:
        db.add(notification)
    db.commit()
    for notification in notifications:
        db.refresh(notification)
    return notifications

def test_create_notification(client, auth_headers, test_user, db):
    """Test creating a new notification"""
    response = client.post(
        "/notifications/",
        json={
            "title": "New Test Notification",
            "message": "This is a new test notification",
            "type": "info"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "Notification created successfully" in data["message"]
    assert "notification_id" in data

    # Verify notification was created in database
    notification = db.query(Notification).filter(Notification.id == data["notification_id"]).first()
    assert notification is not None
    assert notification.title == "New Test Notification"
    assert notification.user_id == test_user.id
    assert notification.is_read == False

def test_create_notification_with_related_entities(client, auth_headers, test_user, db):
    """Test creating notification with related task, client, and opportunity"""
    # Create related entities first
    task = Task(
        title="Test Task",
        description="Test task description",
        assigned_user_id=test_user.id,
        created_by=test_user.id
    )
    db.add(task)

    client_obj = Client(
        name="Test Client",
        email="client@example.com",
        phone="1234567890",
        company_id=test_user.company_id,
        created_by=test_user.id
    )
    db.add(client_obj)

    opportunity = Opportunity(
        title="Test Opportunity",
        value=1000.0,
        client_id=1,
        assigned_user_id=test_user.id,
        created_by=test_user.id
    )
    db.add(opportunity)
    db.commit()

    response = client.post(
        "/notifications/",
        json={
            "title": "Related Notification",
            "message": "Notification with related entities",
            "type": "info",
            "related_task_id": task.id,
            "related_client_id": client_obj.id,
            "related_opportunity_id": opportunity.id
        },
        headers=auth_headers
    )
    assert response.status_code == 200

    # Verify related IDs were stored
    notification_id = response.json()["notification_id"]
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    assert notification.related_task_id == task.id
    assert notification.related_client_id == client_obj.id
    assert notification.related_opportunity_id == opportunity.id

def test_get_notifications(client, auth_headers, test_notifications):
    """Test getting user notifications"""
    response = client.get("/notifications/", headers=auth_headers)
    assert response.status_code == 200
    notifications = response.json()
    assert len(notifications) == 3

    # Check structure of returned notifications
    notification = notifications[0]
    assert "id" in notification
    assert "title" in notification
    assert "message" in notification
    assert "type" in notification
    assert "is_read" in notification
    assert "created_at" in notification

def test_get_notifications_pagination(client, auth_headers, test_notifications):
    """Test pagination of notifications"""
    response = client.get("/notifications/?skip=1&limit=1", headers=auth_headers)
    assert response.status_code == 200
    notifications = response.json()
    assert len(notifications) == 1

def test_get_notifications_filter_by_read_status(client, auth_headers, test_notifications):
    """Test filtering notifications by read status"""
    # Get only unread notifications
    response = client.get("/notifications/?is_read=false", headers=auth_headers)
    assert response.status_code == 200
    notifications = response.json()
    assert len(notifications) == 2  # Two unread notifications
    for notification in notifications:
        assert notification["is_read"] == False

    # Get only read notifications
    response = client.get("/notifications/?is_read=true", headers=auth_headers)
    assert response.status_code == 200
    notifications = response.json()
    assert len(notifications) == 1  # One read notification
    assert notifications[0]["is_read"] == True

def test_get_notifications_filter_by_type(client, auth_headers, test_notifications):
    """Test filtering notifications by type"""
    response = client.get("/notifications/?type_filter=warning", headers=auth_headers)
    assert response.status_code == 200
    notifications = response.json()
    assert len(notifications) == 1
    assert notifications[0]["type"] == "warning"

def test_get_unread_count(client, auth_headers, test_notifications):
    """Test getting count of unread notifications"""
    response = client.get("/notifications/unread/count", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["unread_count"] == 2  # Two unread notifications

def test_update_notification_mark_as_read(client, auth_headers, test_notifications, db):
    """Test marking a notification as read"""
    unread_notification = test_notifications[0]  # First notification is unread

    response = client.put(
        f"/notifications/{unread_notification.id}",
        json={"is_read": True},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "Notification updated successfully" in response.json()["message"]

    # Verify in database
    db.refresh(unread_notification)
    assert unread_notification.is_read == True

def test_update_notification_mark_as_unread(client, auth_headers, test_notifications, db):
    """Test marking a notification as unread"""
    read_notification = test_notifications[1]  # Second notification is read

    response = client.put(
        f"/notifications/{read_notification.id}",
        json={"is_read": False},
        headers=auth_headers
    )
    assert response.status_code == 200

    # Verify in database
    db.refresh(read_notification)
    assert read_notification.is_read == False

def test_update_notification_not_found(client, auth_headers):
    """Test updating non-existent notification"""
    response = client.put(
        "/notifications/999",
        json={"is_read": True},
        headers=auth_headers
    )
    assert response.status_code == 404
    assert "Notification not found" in response.json()["detail"]

def test_update_notification_wrong_user(client, auth_headers, test_notifications, db):
    """Test updating notification that belongs to another user"""
    # Create another user and their notification
    other_user = User(
        name="Other User",
        email="other@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        company_id=1
    )
    db.add(other_user)
    db.commit()

    other_notification = Notification(
        title="Other User Notification",
        message="This belongs to another user",
        type="info",
        user_id=other_user.id,
        is_read=False
    )
    db.add(other_notification)
    db.commit()

    # Try to update it with current user's token
    response = client.put(
        f"/notifications/{other_notification.id}",
        json={"is_read": True},
        headers=auth_headers
    )
    assert response.status_code == 404  # Should not find it

def test_mark_all_read(client, auth_headers, test_notifications, db):
    """Test marking all notifications as read"""
    response = client.put("/notifications/mark-all-read", headers=auth_headers)
    assert response.status_code == 200
    assert "All notifications marked as read" in response.json()["message"]

    # Verify in database
    for notification in test_notifications:
        db.refresh(notification)
        assert notification.is_read == True

def test_delete_notification(client, auth_headers, test_notifications, db):
    """Test deleting a notification"""
    notification_to_delete = test_notifications[0]

    response = client.delete(f"/notifications/{notification_to_delete.id}", headers=auth_headers)
    assert response.status_code == 200
    assert "Notification deleted successfully" in response.json()["message"]

    # Verify deleted from database
    deleted_notification = db.query(Notification).filter(Notification.id == notification_to_delete.id).first()
    assert deleted_notification is None

def test_delete_notification_not_found(client, auth_headers):
    """Test deleting non-existent notification"""
    response = client.delete("/notifications/999", headers=auth_headers)
    assert response.status_code == 404
    assert "Notification not found" in response.json()["detail"]

def test_delete_notification_wrong_user(client, auth_headers, test_notifications, db):
    """Test deleting notification that belongs to another user"""
    # Create another user and their notification
    other_user = User(
        name="Other User",
        email="other@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        company_id=1
    )
    db.add(other_user)
    db.commit()

    other_notification = Notification(
        title="Other User Notification",
        message="This belongs to another user",
        type="info",
        user_id=other_user.id,
        is_read=False
    )
    db.add(other_notification)
    db.commit()

    # Try to delete it with current user's token
    response = client.delete(f"/notifications/{other_notification.id}", headers=auth_headers)
    assert response.status_code == 404  # Should not find it

def test_create_task_notification_function(db, test_user):
    """Test the create_task_notification helper function"""
    from backend.app.routes.notifications import create_task_notification

    # Create a task
    task = Task(
        title="Test Task for Notification",
        description="Test task",
        assigned_user_id=test_user.id,
        created_by=test_user.id
    )
    db.add(task)
    db.commit()

    # Create overdue notification
    create_task_notification(db, task.id, test_user.id, "overdue")

    # Verify notification was created
    notification = db.query(Notification).filter(
        Notification.user_id == test_user.id,
        Notification.related_task_id == task.id
    ).first()
    assert notification is not None
    assert "overdue" in notification.title.lower()
    assert notification.type == "warning"

def test_create_opportunity_notification_function(db, test_user):
    """Test the create_opportunity_notification helper function"""
    from backend.app.routes.notifications import create_opportunity_notification

    # Create an opportunity
    opportunity = Opportunity(
        title="Test Opportunity",
        value=5000.0,
        client_id=1,
        assigned_user_id=test_user.id,
        created_by=test_user.id,
        stage="proposal"
    )
    db.add(opportunity)
    db.commit()

    # Create won notification
    create_opportunity_notification(db, opportunity.id, test_user.id, "won")

    # Verify notification was created
    notification = db.query(Notification).filter(
        Notification.user_id == test_user.id,
        Notification.related_opportunity_id == opportunity.id
    ).first()
    assert notification is not None
    assert "won" in notification.title.lower()
    assert notification.type == "success"

def test_create_client_notification_function(db, test_user):
    """Test the create_client_notification helper function"""
    from backend.app.routes.notifications import create_client_notification

    # Create a client
    client_obj = Client(
        name="Test Client for Notification",
        email="client@example.com",
        phone="1234567890",
        company_id=test_user.company_id,
        created_by=test_user.id
    )
    db.add(client_obj)
    db.commit()

    # Create new client notification
    create_client_notification(db, client_obj.id, test_user.id, "new_client")

    # Verify notification was created
    notification = db.query(Notification).filter(
        Notification.user_id == test_user.id,
        Notification.related_client_id == client_obj.id
    ).first()
    assert notification is not None
    assert "new client" in notification.title.lower()
    assert notification.type == "info"

def test_notification_created_at_and_updated_at(client, auth_headers, db, test_user):
    """Test that created_at and updated_at timestamps are set correctly"""
    response = client.post(
        "/notifications/",
        json={
            "title": "Timestamp Test",
            "message": "Testing timestamps",
            "type": "info"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    notification_id = response.json()["notification_id"]

    # Check created_at was set
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    assert notification.created_at is not None
    assert notification.updated_at is None  # Should be None initially

    # Update the notification and check updated_at
    import time
    time.sleep(1)  # Small delay to ensure different timestamp

    client.put(
        f"/notifications/{notification_id}",
        json={"is_read": True},
        headers=auth_headers
    )

    db.refresh(notification)
    assert notification.updated_at is not None
    assert notification.updated_at > notification.created_at

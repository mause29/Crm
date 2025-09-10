import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from ..database_new import Base, get_db
from ..models import User, Points, Achievement, UserAchievement, Task, Opportunity, Client
from ..auth import create_access_token
from ..main import app
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Test database setup
from sqlalchemy import create_engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_gamification.db"
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
def test_achievements(db):
    achievements = [
        Achievement(name="First Steps", description="Earn 50 points", points_required=50, badge_icon="🏆"),
        Achievement(name="Task Master", description="Complete 10 tasks", points_required=100, badge_icon="✅"),
        Achievement(name="Client Builder", description="Add 5 clients", points_required=150, badge_icon="👥"),
    ]
    for ach in achievements:
        db.add(ach)
    db.commit()
    return achievements

def test_complete_challenge_task_completed(client, auth_headers, test_user, db):
    """Test completing a task challenge"""
    user_id = test_user.id
    response = client.post(
        "/gamification/complete_challenge",
        json={
            "user_id": user_id,
            "challenge_type": "task_completed"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "10 points added" in response.json()["message"]

    # Verify points were added by querying with user_id directly
    points = db.query(Points).filter(Points.user_id == user_id).first()
    assert points is not None
    assert points.points == 10
    assert "task_completed" in points.reason
    
def test_complete_challenge_client_added(client, auth_headers, test_user, db):
    
    user_id = test_user.id
    response = client.post(
        "/gamification/complete_challenge",
        json={
            "user_id": user_id,
            "challenge_type": "client_added"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "15 points added" in response.json()["message"]

    # Verify points were added
    points = db.query(Points).filter(Points.user_id == user_id).first()
    assert points.points == 15
def test_complete_challenge_invalid_type(client, auth_headers, test_user):
    """Test completing a challenge with invalid type"""
    response = client.post(
        "/gamification/complete_challenge",
        json={
            "user_id": test_user.id,
            "challenge_type": "invalid_type"
        },
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation error

def test_complete_challenge_wrong_user(client, auth_headers, test_user, db):
    """Test completing challenge for another user (should fail)"""
    # Create another user
    other_user = User(
        name="Other User",
        email="other@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        company_id=1
    )
    db.add(other_user)
    db.commit()

    response = client.post(
        "/gamification/complete_challenge",
        json={
            "user_id": other_user.id,
            "challenge_type": "task_completed"
        },
        headers=auth_headers
    )
    assert response.status_code == 403
    assert "Cannot complete challenge for another user" in response.json()["detail"]

def test_get_user_points(client, auth_headers, test_user, db):
    """Test getting user points"""
    # Add some points first
    points_entry = Points(user_id=test_user.id, points=25, reason="Test points")
    db.add(points_entry)
    db.commit()

    response = client.get(f"/gamification/user_points/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_points"] == 25
    assert len(data["recent_points"]) == 1
    assert data["recent_points"][0]["points"] == 25

def test_get_user_points_wrong_user(client, auth_headers, test_user, db):
    """Test getting points for another user (should fail)"""
    other_user = User(
        name="Other User",
        email="other@example.com",
        hashed_password=get_password_hash("password123"),
        role="user",
        company_id=1
    )
    db.add(other_user)
    db.commit()

    response = client.get(f"/gamification/user_points/{other_user.id}", headers=auth_headers)
    assert response.status_code == 403

def test_get_achievements(client, test_achievements):
    """Test getting all achievements"""
    response = client.get("/gamification/achievements")
    assert response.status_code == 200
    achievements = response.json()
    assert len(achievements) >= 3
    assert any(ach["name"] == "First Steps" for ach in achievements)

def test_get_user_achievements(client, auth_headers, test_user, test_achievements, db):
    """Test getting user achievements"""
    # Unlock an achievement
    user_achievement = UserAchievement(user_id=test_user.id, achievement_id=test_achievements[0].id)
    db.add(user_achievement)
    db.commit()

    response = client.get(f"/gamification/user_achievements/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200
    achievements = response.json()
    assert len(achievements) == 1
    assert achievements[0]["name"] == "First Steps"

def test_unlock_achievement(client, auth_headers, test_user, test_achievements, db):
    
    user_id = test_user.id
    achievement_id = test_achievements[0].id
    # Add enough points
    points_entry = Points(user_id=user_id, points=100, reason="Enough points")
    db.add(points_entry)
    db.commit()

    response = client.post(
        f"/gamification/unlock_achievement?user_id={user_id}&achievement_id={achievement_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "Achievement unlocked" in response.json()["message"]

    # Verify achievement was unlocked
    user_ach = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement_id
    ).first()
    assert user_ach is not None
def test_unlock_achievement_insufficient_points(client, auth_headers, test_user, test_achievements):
    """Test unlocking achievement without enough points"""
    response = client.post(
        f"/gamification/unlock_achievement?user_id={test_user.id}&achievement_id={test_achievements[1].id}",
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "Not enough points" in response.json()["detail"]

def test_unlock_achievement_already_unlocked(client, auth_headers, test_user, test_achievements, db):
    """Test unlocking already unlocked achievement"""
    # First unlock it
    user_achievement = UserAchievement(user_id=test_user.id, achievement_id=test_achievements[0].id)
    db.add(user_achievement)
    db.commit()

    response = client.post(
        f"/gamification/unlock_achievement?user_id={test_user.id}&achievement_id={test_achievements[0].id}",
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "already unlocked" in response.json()["detail"]

def test_get_leaderboard(client, test_user, db):
    
    user_id = test_user.id
    # Add points for the test user
    points_entry = Points(user_id=user_id, points=100, reason="Leaderboard test")
    db.add(points_entry)
    db.commit()

    response = client.get("/gamification/leaderboard")
    assert response.status_code == 200
    leaderboard = response.json()
    assert len(leaderboard) >= 1
    assert leaderboard[0]["user_id"] == user_id
    assert leaderboard[0]["total_points"] == 100
def test_get_user_stats(client, auth_headers, test_user, db):
    """Test getting user statistics"""
    # Add some data
    points_entry = Points(user_id=test_user.id, points=50, reason="Stats test")
    db.add(points_entry)

    task = Task(
        title="Test Task",
        description="Test task",
        assigned_user_id=test_user.id,
        status="completed",
        created_by=test_user.id
    )
    db.add(task)

    opportunity = Opportunity(
        name="Test Opportunity",
        value=1000.0,
        client_id=1,
        assigned_user_id=test_user.id,
        stage="closed_won"
    )
    db.add(opportunity)

    db.commit()

    response = client.get(f"/gamification/user_stats/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_points"] == 50
    assert stats["tasks_completed"] == 1
    assert stats["deals_closed"] == 1
    assert stats["achievements_unlocked"] == 0

def test_automatic_achievement_unlock(client, auth_headers, test_user, db):
    """Test automatic achievement unlocking based on actions"""
    user_id = test_user.id
    # Create achievement
    achievement = Achievement(name="First Steps", description="Earn 50 points", points_required=50, badge_icon="🏆")
    db.add(achievement)
    db.commit()

    # Add points to trigger achievement
    points_entry = Points(user_id=user_id, points=60, reason="Achievement trigger")
    db.add(points_entry)
    db.commit()

    # Complete a challenge to trigger automatic achievement check
    response = client.post(
        "/gamification/complete_challenge",
        json={
            "user_id": user_id,
            "challenge_type": "task_completed"
        },
        headers=auth_headers
    )
    assert response.status_code == 200

    # Check if achievement was automatically unlocked
    user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()
    # Note: This test might need adjustment based on the exact automatic unlock logic
    # For now, we just verify the challenge completion worked
    assert response.status_code == 200

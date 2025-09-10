from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..database_new import get_db
from ..models import Points, Achievement, UserAchievement, User, Task, Opportunity, Client
from ..auth import get_current_user
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/gamification", tags=["gamification"])

class CompleteChallengeRequest(BaseModel):
    user_id: int
    challenge_type: str  # e.g., "task_completed", "client_added", "deal_closed"

    @validator('challenge_type')
    def validate_challenge_type(cls, v):
        valid_types = ["task_completed", "client_added", "deal_closed", "login_streak", "first_sale"]
        if v not in valid_types:
            raise ValueError(f'Challenge type must be one of {valid_types}')
        return v

class AchievementCreate(BaseModel):
    name: str
    description: str
    points_required: int
    icon: Optional[str] = None

@router.post("/complete_challenge")
def complete_challenge(request: CompleteChallengeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validate user access
    if request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot complete challenge for another user")

    # Determine points based on challenge type
    points_map = {
        "task_completed": 10,
        "client_added": 15,
        "deal_closed": 50,
        "login_streak": 5,
        "first_sale": 100
    }
    points = points_map.get(request.challenge_type, 10)

    # Add points for completing challenge
    points_entry = Points(user_id=request.user_id, points=points, reason=f"Completed {request.challenge_type} challenge")
    db.add(points_entry)

    # Check for automatic achievement unlocks
    check_and_unlock_achievements(request.user_id, db)

    db.commit()
    return {"message": f"Challenge completed, {points} points added"}

@router.get("/user_points/{user_id}")
def get_user_points(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if user can view points
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot view points for another user")

    total_points = db.query(func.sum(Points.points)).filter(Points.user_id == user_id).scalar() or 0
    recent_points = db.query(Points).filter(Points.user_id == user_id).order_by(Points.created_at.desc()).limit(5).all()

    return {
        "total_points": total_points,
        "recent_points": [{"points": p.points, "reason": p.reason, "created_at": p.created_at} for p in recent_points]
    }

@router.get("/achievements")
def get_achievements(db: Session = Depends(get_db)):
    achievements = db.query(Achievement).all()
    return [{"id": a.id, "name": a.name, "description": a.description, "points_required": a.points_required, "icon": a.badge_icon} for a in achievements]

@router.get("/user_achievements/{user_id}")
def get_user_achievements(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot view achievements for another user")

    user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()
    achievements = []
    for ua in user_achievements:
        achievement = db.query(Achievement).filter(Achievement.id == ua.achievement_id).first()
        if achievement:
            achievements.append({
                "id": ua.id,
                "achievement_id": ua.achievement_id,
                "name": achievement.name,
                "description": achievement.description,
                "unlocked_at": ua.unlocked_at,
                "icon": achievement.badge_icon
            })
    return achievements

@router.post("/unlock_achievement")
def unlock_achievement(user_id: int, achievement_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot unlock achievement for another user")

    # Check if already unlocked
    existing = db.query(UserAchievement).filter(UserAchievement.user_id == user_id, UserAchievement.achievement_id == achievement_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Achievement already unlocked")

    # Check if user has enough points
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")

    total_points = db.query(func.sum(Points.points)).filter(Points.user_id == user_id).scalar() or 0
    if total_points < achievement.points_required:
        raise HTTPException(status_code=400, detail="Not enough points to unlock this achievement")

    user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement_id)
    db.add(user_achievement)
    db.commit()
    return {"message": "Achievement unlocked"}

@router.get("/leaderboard")
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Get top users by points"""
    leaderboard = db.query(
        User.id,
        User.name,
        User.email,
        func.sum(Points.points).label('total_points')
    ).join(Points, User.id == Points.user_id).group_by(User.id).order_by(desc(func.sum(Points.points))).limit(limit).all()

    return [
        {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "total_points": user.total_points
        } for user in leaderboard
    ]

@router.get("/user_stats/{user_id}")
def get_user_stats(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot view stats for another user")

    total_points = db.query(func.sum(Points.points)).filter(Points.user_id == user_id).scalar() or 0
    achievements_count = db.query(UserAchievement).filter(UserAchievement.user_id == user_id).count()
    tasks_completed = db.query(Task).filter(Task.assigned_user_id == user_id, Task.status == "completed").count()
    deals_closed = db.query(Opportunity).filter(Opportunity.assigned_user_id == user_id, Opportunity.stage == "closed_won").count()

    return {
        "total_points": total_points,
        "achievements_unlocked": achievements_count,
        "tasks_completed": tasks_completed,
        "deals_closed": deals_closed
    }

def check_and_unlock_achievements(user_id: int, db: Session):
    """Automatically check and unlock achievements based on user actions"""
    # Get user stats
    total_points = db.query(func.sum(Points.points)).filter(Points.user_id == user_id).scalar() or 0
    tasks_completed = db.query(Task).filter(Task.assigned_user_id == user_id, Task.status == "completed").count()
    clients_added = db.query(Client).filter(Client.created_by == user_id).count()
    deals_closed = db.query(Opportunity).filter(Opportunity.assigned_user_id == user_id, Opportunity.stage == "closed_won").count()

    # Define achievement conditions
    achievements_to_check = [
        {"name": "First Steps", "condition": total_points >= 50, "points_required": 50},
        {"name": "Task Master", "condition": tasks_completed >= 10, "points_required": 100},
        {"name": "Client Builder", "condition": clients_added >= 5, "points_required": 150},
        {"name": "Deal Closer", "condition": deals_closed >= 3, "points_required": 200},
        {"name": "CRM Champion", "condition": total_points >= 500, "points_required": 500}
    ]

    for ach_data in achievements_to_check:
        achievement = db.query(Achievement).filter(Achievement.name == ach_data["name"]).first()
        if achievement:
            existing = db.query(UserAchievement).filter(UserAchievement.user_id == user_id, UserAchievement.achievement_id == achievement.id).first()
            if not existing and ach_data["condition"]:
                user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement.id)
                db.add(user_achievement)
                db.commit()

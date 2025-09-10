from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from ..database_new import get_db
from ..models import User, Notification, Task, Opportunity, Client
from ..auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

class NotificationCreate(BaseModel):
    title: str
    message: str
    type: str = "info"  # info, warning, success, error
    related_task_id: Optional[int] = None
    related_client_id: Optional[int] = None
    related_opportunity_id: Optional[int] = None

class NotificationUpdate(BaseModel):
    is_read: bool = False

@router.post("/", response_model=dict)
def create_notification(
    notification: NotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new notification"""

    db_notification = Notification(
        title=notification.title,
        message=notification.message,
        type=notification.type,
        user_id=current_user.id,
        related_task_id=notification.related_task_id,
        related_client_id=notification.related_client_id,
        related_opportunity_id=notification.related_opportunity_id
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return {"message": "Notification created successfully", "notification_id": db_notification.id}

@router.get("/", response_model=List[dict])
def get_notifications(
    skip: int = 0,
    limit: int = 50,
    is_read: Optional[bool] = None,
    type_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user notifications with optional filtering"""

    query = db.query(Notification).filter(Notification.user_id == current_user.id)

    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)

    if type_filter:
        query = query.filter(Notification.type == type_filter)

    notifications = query.order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()

    return [
        {
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "type": notification.type,
            "is_read": notification.is_read,
            "created_at": notification.created_at,
            "related_task_id": notification.related_task_id,
            "related_client_id": notification.related_client_id,
            "related_opportunity_id": notification.related_opportunity_id
        }
        for notification in notifications
    ]

@router.get("/unread/count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of unread notifications"""

    count = db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
    ).count()

    return {"unread_count": count}

@router.put("/{notification_id}")
def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update notification (mark as read/unread)"""

    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = notification_update.is_read
    notification.updated_at = datetime.utcnow()

    db.commit()

    return {"message": "Notification updated successfully"}

@router.put("/mark-all-read")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read"""

    db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
    ).update({"is_read": True, "updated_at": datetime.utcnow()})

    db.commit()

    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a notification"""

    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()

    return {"message": "Notification deleted successfully"}

# Automated notification functions
def create_task_notification(db: Session, task_id: int, user_id: int, notification_type: str):
    """Create automated task-related notifications"""

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return

    if notification_type == "overdue":
        title = f"Task Overdue: {task.title}"
        message = f"The task '{task.title}' is now overdue. Please review and update its status."
        notification_type_db = "warning"
    elif notification_type == "due_soon":
        title = f"Task Due Soon: {task.title}"
        message = f"The task '{task.title}' is due within 24 hours."
        notification_type_db = "warning"
    elif notification_type == "completed":
        title = f"Task Completed: {task.title}"
        message = f"Great job! The task '{task.title}' has been completed."
        notification_type_db = "success"
    else:
        return

    notification = Notification(
        title=title,
        message=message,
        type=notification_type_db,
        user_id=user_id,
        related_task_id=task_id
    )

    db.add(notification)
    db.commit()

def create_opportunity_notification(db: Session, opportunity_id: int, user_id: int, notification_type: str):
    """Create automated opportunity-related notifications"""

    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        return

    if notification_type == "stage_changed":
        title = f"Opportunity Updated: {opportunity.title}"
        message = f"The opportunity '{opportunity.title}' has moved to '{opportunity.stage}' stage."
        notification_type_db = "info"
    elif notification_type == "won":
        title = f"🎉 Opportunity Won: {opportunity.title}"
        message = f"Congratulations! The opportunity '{opportunity.title}' has been won with value ${opportunity.value}."
        notification_type_db = "success"
    elif notification_type == "lost":
        title = f"Opportunity Lost: {opportunity.title}"
        message = f"The opportunity '{opportunity.title}' has been lost. Review and learn from this experience."
        notification_type_db = "warning"
    else:
        return

    notification = Notification(
        title=title,
        message=message,
        type=notification_type_db,
        user_id=user_id,
        related_opportunity_id=opportunity_id
    )

    db.add(notification)
    db.commit()

def create_client_notification(db: Session, client_id: int, user_id: int, notification_type: str):
    """Create automated client-related notifications"""

    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return

    if notification_type == "new_client":
        title = f"New Client Added: {client.name}"
        message = f"A new client '{client.name}' has been added to your CRM."
        notification_type_db = "info"
    elif notification_type == "client_updated":
        title = f"Client Updated: {client.name}"
        message = f"The client '{client.name}' information has been updated."
        notification_type_db = "info"
    else:
        return

    notification = Notification(
        title=title,
        message=message,
        type=notification_type_db,
        user_id=user_id,
        related_client_id=client_id
    )

    db.add(notification)
    db.commit()

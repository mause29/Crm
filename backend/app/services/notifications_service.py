from typing import List
from pydantic import BaseModel

class Notification(BaseModel):
    id: int
    message: str
    user_id: int

notifications_db: List[Notification] = []

def get_notifications_for_user(user_id: int) -> List[Notification]:
    return [n for n in notifications_db if n.user_id == user_id]

def add_notification(notification: Notification) -> Notification:
    notifications_db.append(notification)
    return notification

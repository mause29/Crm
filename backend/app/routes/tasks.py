from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from ..database_new import get_db
from ..models import User, Task
from ..auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: str = "medium"  # low, medium, high
    status: str = "pending"  # pending, in_progress, completed, cancelled
    assigned_to: Optional[int] = None
    related_client_id: Optional[int] = None
    related_opportunity_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None

@router.post("/", response_model=dict)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority,
        status=task.status,
        created_by=current_user.id,
        assigned_user_id=task.assigned_to or current_user.id,
        related_client_id=task.related_client_id,
        related_opportunity_id=task.related_opportunity_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return {"message": "Task created successfully", "task_id": db_task.id}

@router.get("/", response_model=List[dict])
def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to:
        query = query.filter(Task.assigned_user_id == assigned_to)
    else:
        # Show tasks assigned to current user or created by them
        query = query.filter(
            (Task.assigned_user_id == current_user.id) | (Task.created_by == current_user.id)
        )

    tasks = query.order_by(Task.due_date.asc(), Task.priority.desc()).all()

    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "priority": task.priority,
            "status": task.status,
            "created_by": task.created_by,
            "assigned_to": task.assigned_user_id,
            "related_client_id": task.related_client_id,
            "related_opportunity_id": task.related_opportunity_id,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
        for task in tasks
    ]

@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if user has access to this task
    if task.assigned_user_id != current_user.id and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date,
        "priority": task.priority,
        "status": task.status,
        "created_by": task.created_by,
        "assigned_to": task.assigned_user_id,
        "related_client_id": task.related_client_id,
        "related_opportunity_id": task.related_opportunity_id,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }

@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if user has access to update this task
    if task.assigned_user_id != current_user.id and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Task updated successfully"}

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if user has access to delete this task
    if task.assigned_user_id != current_user.id and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@router.get("/stats/overview")
def get_task_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task statistics for the current user"""
    tasks = db.query(Task).filter(
        (Task.assigned_user_id == current_user.id) | (Task.created_by == current_user.id)
    ).all()

    stats = {
        "total": len(tasks),
        "pending": len([t for t in tasks if t.status == "pending"]),
        "in_progress": len([t for t in tasks if t.status == "in_progress"]),
        "completed": len([t for t in tasks if t.status == "completed"]),
        "overdue": len([t for t in tasks if t.due_date and t.due_date < date.today() and t.status != "completed"]),
        "high_priority": len([t for t in tasks if t.priority == "high" and t.status != "completed"]),
        "due_today": len([t for t in tasks if t.due_date == date.today() and t.status != "completed"])
    }

    return stats

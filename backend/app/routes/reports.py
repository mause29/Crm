from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, extract, between
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from ..database_new import get_db
from ..models import User, Client, Opportunity, Task, Invoice, Points, Achievement, UserAchievement
from ..auth import get_current_user
import json

router = APIRouter(prefix="/reports", tags=["reports"])

class ReportFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_id: Optional[int] = None
    client_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None

@router.get("/sales/summary")
def get_sales_summary(
    period: str = "monthly",
    months: int = 12,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate sales performance summary report"""

    if period == "monthly":
        # Monthly sales data
        sales_data = db.query(
            extract('year', Invoice.created_at).label('year'),
            extract('month', Invoice.created_at).label('month'),
            func.sum(Invoice.amount).label('total_amount'),
            func.count(Invoice.id).label('invoice_count')
        ).filter(
            and_(
                Invoice.status == "paid",
                Invoice.created_at >= datetime.utcnow() - timedelta(days=months*30)
            )
        ).group_by(
            extract('year', Invoice.created_at),
            extract('month', Invoice.created_at)
        ).order_by(
            extract('year', Invoice.created_at),
            extract('month', Invoice.created_at)
        ).all()

        # Opportunity conversion data
        opportunities_data = db.query(
            extract('year', Opportunity.created_at).label('year'),
            extract('month', Opportunity.created_at).label('month'),
            func.count(Opportunity.id).label('total_opportunities'),
            func.count(Opportunity.id).filter(Opportunity.stage == "closed_won").label('won_opportunities')
        ).filter(
            Opportunity.created_at >= datetime.utcnow() - timedelta(days=months*30)
        ).group_by(
            extract('year', Opportunity.created_at),
            extract('month', Opportunity.created_at)
        ).order_by(
            extract('year', Opportunity.created_at),
            extract('month', Opportunity.created_at)
        ).all()

        return {
            "sales_trend": [
                {
                    "period": f"{int(row.year)}-{int(row.month):02d}",
                    "revenue": float(row.total_amount or 0),
                    "invoice_count": row.invoice_count
                }
                for row in sales_data
            ],
            "conversion_trend": [
                {
                    "period": f"{int(row.year)}-{int(row.month):02d}",
                    "total_opportunities": row.total_opportunities,
                    "won_opportunities": row.won_opportunities,
                    "conversion_rate": (row.won_opportunities / row.total_opportunities * 100) if row.total_opportunities > 0 else 0
                }
                for row in opportunities_data
            ]
        }

    return {"message": "Invalid period specified"}

@router.get("/tasks/productivity")
def get_task_productivity_report(
    user_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate task productivity report"""

    query = db.query(Task)

    if user_id:
        query = query.filter(Task.assigned_user_id == user_id)
    elif current_user.role != "admin":
        query = query.filter(Task.assigned_user_id == current_user.id)

    if start_date:
        query = query.filter(Task.created_at >= start_date)
    if end_date:
        query = query.filter(Task.created_at <= end_date)

    tasks = query.all()

    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == "completed"])
    overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != "completed"])

    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    overdue_rate = (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Tasks by priority
    priority_stats = {}
    for task in tasks:
        priority = getattr(task, 'priority', 'medium')
        if priority not in priority_stats:
            priority_stats[priority] = {'total': 0, 'completed': 0}
        priority_stats[priority]['total'] += 1
        if task.status == "completed":
            priority_stats[priority]['completed'] += 1

    # Tasks by status
    status_stats = {}
    for task in tasks:
        status = task.status
        if status not in status_stats:
            status_stats[status] = 0
        status_stats[status] += 1

    return {
        "summary": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,
            "completion_rate": completion_rate,
            "overdue_rate": overdue_rate
        },
        "by_priority": priority_stats,
        "by_status": status_stats
    }

@router.get("/clients/insights")
def get_client_insights_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate client insights report"""

    # Client acquisition over time
    client_acquisition = db.query(
        extract('year', Client.created_at).label('year'),
        extract('month', Client.created_at).label('month'),
        func.count(Client.id).label('new_clients')
    ).group_by(
        extract('year', Client.created_at),
        extract('month', Client.created_at)
    ).order_by(
        extract('year', Client.created_at),
        extract('month', Client.created_at)
    ).all()

    # Revenue by client
    client_revenue = db.query(
        Client.name,
        Client.email,
        func.sum(Invoice.amount).label('total_revenue'),
        func.count(Invoice.id).label('invoice_count'),
        func.max(Invoice.created_at).label('last_invoice_date')
    ).join(Invoice).filter(
        Invoice.status == "paid"
    ).group_by(Client.id, Client.name, Client.email).order_by(
        desc(func.sum(Invoice.amount))
    ).limit(20).all()

    # Client engagement (opportunities per client)
    client_engagement = db.query(
        Client.name,
        func.count(Opportunity.id).label('total_opportunities'),
        func.count(Opportunity.id).filter(Opportunity.stage == "closed_won").label('won_opportunities'),
        func.avg(Opportunity.value).label('avg_opportunity_value')
    ).join(Opportunity).group_by(Client.id, Client.name).order_by(
        desc(func.count(Opportunity.id))
    ).limit(20).all()

    return {
        "acquisition_trend": [
            {
                "period": f"{int(row.year)}-{int(row.month):02d}",
                "new_clients": row.new_clients
            }
            for row in client_acquisition
        ],
        "top_clients_by_revenue": [
            {
                "name": row.name,
                "email": row.email,
                "total_revenue": float(row.total_revenue),
                "invoice_count": row.invoice_count,
                "last_invoice_date": row.last_invoice_date
            }
            for row in client_revenue
        ],
        "client_engagement": [
            {
                "name": row.name,
                "total_opportunities": row.total_opportunities,
                "won_opportunities": row.won_opportunities,
                "conversion_rate": (row.won_opportunities / row.total_opportunities * 100) if row.total_opportunities > 0 else 0,
                "avg_opportunity_value": float(row.avg_opportunity_value or 0)
            }
            for row in client_engagement
        ]
    }

@router.get("/gamification/leaderboard")
def get_gamification_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate gamification leaderboard report"""

    # Points leaderboard
    points_leaderboard = db.query(
        User.email,
        func.sum(Points.points).label('total_points'),
        func.count(Points.id).label('activities_count'),
        func.max(Points.created_at).label('last_activity')
    ).join(User).group_by(User.id, User.email).order_by(
        desc(func.sum(Points.points))
    ).limit(limit).all()

    # Achievement distribution
    achievement_stats = db.query(
        Achievement.name,
        Achievement.description,
        func.count(UserAchievement.id).label('unlocked_count')
    ).join(UserAchievement).group_by(Achievement.id, Achievement.name, Achievement.description).order_by(
        desc(func.count(UserAchievement.id))
    ).all()

    # User achievements
    user_achievements = db.query(
        User.email,
        func.count(UserAchievement.id).label('achievement_count'),
        func.max(UserAchievement.unlocked_at).label('last_achievement_date')
    ).join(UserAchievement).group_by(User.id, User.email).order_by(
        desc(func.count(UserAchievement.id))
    ).limit(limit).all()

    return {
        "points_leaderboard": [
            {
                "user": row.email,
                "total_points": row.total_points,
                "activities_count": row.activities_count,
                "last_activity": row.last_activity
            }
            for row in points_leaderboard
        ],
        "achievement_distribution": [
            {
                "achievement_name": row.name,
                "description": row.description,
                "unlocked_count": row.unlocked_count
            }
            for row in achievement_stats
        ],
        "user_achievements": [
            {
                "user": row.email,
                "achievement_count": row.achievement_count,
                "last_achievement_date": row.last_achievement_date
            }
            for row in user_achievements
        ]
    }

@router.get("/performance/dashboard")
def get_performance_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate comprehensive performance dashboard"""

    # Overall metrics
    total_clients = db.query(func.count(Client.id)).scalar()
    total_opportunities = db.query(func.count(Opportunity.id)).scalar()
    total_revenue = db.query(func.sum(Invoice.amount)).filter(Invoice.status == "paid").scalar() or 0
    total_tasks = db.query(func.count(Task.id)).scalar()

    # Monthly growth
    this_month = datetime.utcnow().replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)

    # For now, we'll use total clients since created_at column doesn't exist in database
    this_month_clients = 0  # Placeholder - would need migration to add created_at column
    last_month_clients = 0  # Placeholder - would need migration to add created_at column

    this_month_revenue = db.query(func.sum(Invoice.amount)).filter(
        and_(Invoice.status == "paid", Invoice.created_at >= this_month)
    ).scalar() or 0

    last_month_revenue = db.query(func.sum(Invoice.amount)).filter(
        and_(Invoice.status == "paid", Invoice.created_at >= last_month, Invoice.created_at < this_month)
    ).scalar() or 0

    # Calculate growth rates
    client_growth = ((this_month_clients - last_month_clients) / last_month_clients * 100) if last_month_clients > 0 else 0
    revenue_growth = ((this_month_revenue - last_month_revenue) / last_month_revenue * 100) if last_month_revenue > 0 else 0

    # Top performers
    top_sales_users = db.query(
        User.email,
        func.sum(Invoice.amount).label('total_sales')
    ).join(Invoice, User.id == Invoice.client_id).filter(
        Invoice.status == "paid"
    ).group_by(User.id, User.email).order_by(
        desc(func.sum(Invoice.amount))
    ).limit(5).all()

    return {
        "overall_metrics": {
            "total_clients": total_clients,
            "total_opportunities": total_opportunities,
            "total_revenue": float(total_revenue),
            "total_tasks": total_tasks
        },
        "monthly_growth": {
            "client_growth": client_growth,
            "revenue_growth": revenue_growth,
            "this_month_clients": this_month_clients,
            "this_month_revenue": float(this_month_revenue)
        },
        "top_performers": [
            {
                "user": row.email,
                "total_sales": float(row.total_sales)
            }
            for row in top_sales_users
        ]
    }

@router.get("/export/{report_type}")
def export_report(
    report_type: str,
    format: str = "json",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export reports in various formats"""

    if report_type == "sales":
        data = get_sales_summary(db=db, current_user=current_user)
    elif report_type == "tasks":
        data = get_task_productivity_report(db=db, current_user=current_user)
    elif report_type == "clients":
        data = get_client_insights_report(db=db, current_user=current_user)
    elif report_type == "gamification":
        data = get_gamification_leaderboard(db=db, current_user=current_user)
    elif report_type == "performance":
        data = get_performance_dashboard(db=db, current_user=current_user)
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

    if format == "json":
        return data
    else:
        # For other formats, you could implement CSV, PDF, etc.
        raise HTTPException(status_code=400, detail="Format not supported yet")

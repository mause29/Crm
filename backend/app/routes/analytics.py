from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, or_
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..database_new import get_db
from ..models import User, Client, Opportunity, Task, Invoice, Points
from ..auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard/overview")
def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive dashboard overview with key metrics"""

    # Date ranges
    today = datetime.utcnow().date()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)

    # Revenue metrics
    total_revenue = db.query(func.sum(Invoice.amount)).filter(
        Invoice.status == "paid"
    ).scalar() or 0

    monthly_revenue = db.query(func.sum(Invoice.amount)).filter(
        and_(
            Invoice.status == "paid",
            Invoice.created_at >= this_month_start
        )
    ).scalar() or 0

    # Client metrics
    total_clients = db.query(Client).count()
    new_clients_this_month = db.query(Client).filter(
        Client.created_at >= this_month_start
    ).count()

    # Opportunity metrics
    total_opportunities = db.query(Opportunity).count()

    # Task metrics
    total_tasks = db.query(Task).filter(
        or_(
            Task.assigned_user_id == current_user.id,
            Task.created_by == current_user.id
        )
    ).count()

    completed_tasks = db.query(Task).filter(
        and_(
            or_(
                Task.assigned_user_id == current_user.id,
                Task.created_by == current_user.id
            ),
            Task.status == "completed"
        )
    ).count()

    return {
        "revenue": {
            "total": float(total_revenue),
            "monthly": float(monthly_revenue)
        },
        "clients": {
            "total": total_clients,
            "new_this_month": new_clients_this_month
        },
        "opportunities": {
            "total": total_opportunities
        },
        "tasks": {
            "total": total_tasks,
            "completed": completed_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
    }

@router.get("/revenue/chart")
def get_revenue_chart(
    period: str = "monthly",
    months: int = 12,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get revenue data for charts"""

    if period == "monthly":
        result = db.query(
            extract('year', Invoice.created_at).label('year'),
            extract('month', Invoice.created_at).label('month'),
            func.sum(Invoice.amount).label('revenue')
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

        return [
            {
                "period": f"{int(row.year)}-{int(row.month):02d}",
                "revenue": float(row.revenue)
            }
            for row in result
        ]

    return []

@router.get("/performance/metrics")
def get_performance_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get performance metrics for the current user"""

    # Opportunity conversion rate
    opportunities_created = db.query(Opportunity).filter(
        Opportunity.assigned_user_id == current_user.id
    ).count()

    opportunities_won = db.query(Opportunity).filter(
        and_(
            Opportunity.assigned_user_id == current_user.id,
            Opportunity.stage == "closed_won"
        )
    ).count()

    conversion_rate = (opportunities_won / opportunities_created * 100) if opportunities_created > 0 else 0

    return {
        "sales_performance": {
            "opportunities_created": opportunities_created,
            "opportunities_won": opportunities_won,
            "conversion_rate": conversion_rate
        }
    }

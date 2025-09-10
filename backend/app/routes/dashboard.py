from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from ..database_new import get_db
from ..models import User, Client, Opportunity, Invoice, Points
from ..auth import get_current_user
from datetime import datetime, timedelta
from typing import List, Dict, Any

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/metrics")
def get_dashboard_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get main dashboard metrics"""
    # Total clients
    total_clients = db.query(Client).filter(Client.company_id == current_user.company_id).count()

    # Total opportunities (filter by assigned user since Opportunity doesn't have company_id)
    total_opportunities = db.query(Opportunity).filter(Opportunity.assigned_user_id == current_user.id).count()

    # Total revenue (from paid invoices for clients in user's company)
    client_ids = [c.id for c in db.query(Client).filter(Client.company_id == current_user.company_id).all()]
    total_revenue = db.query(func.sum(Invoice.amount)).filter(
        and_(
            Invoice.client_id.in_(client_ids),
            Invoice.status == 'paid'
        )
    ).scalar() or 0

    # Active opportunities (not closed)
    active_opportunities = db.query(Opportunity).filter(
        and_(
            Opportunity.assigned_user_id == current_user.id,
            Opportunity.stage != 'Closed Won',
            Opportunity.stage != 'Closed Lost'
        )
    ).count()

    # Monthly revenue (current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_revenue = db.query(func.sum(Invoice.amount)).filter(
        and_(
            Invoice.client_id.in_(client_ids),
            Invoice.status == 'paid',
            extract('month', Invoice.created_at) == current_month,
            extract('year', Invoice.created_at) == current_year
        )
    ).scalar() or 0

    # User points (gamification)
    user_points = db.query(func.sum(Points.points)).filter(
        Points.user_id == current_user.id
    ).scalar() or 0

    return {
        "total_clients": total_clients,
        "total_opportunities": total_opportunities,
        "total_revenue": float(total_revenue),
        "active_opportunities": active_opportunities,
        "monthly_revenue": float(monthly_revenue),
        "user_points": user_points
    }

@router.get("/sales-funnel")
def get_sales_funnel(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sales funnel data by stage"""
    stages = ['Lead', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']

    funnel_data = []
    for stage in stages:
        count = db.query(Opportunity).filter(
            and_(
                Opportunity.assigned_user_id == current_user.id,
                Opportunity.stage == stage
            )
        ).count()

        value = db.query(func.sum(Opportunity.value)).filter(
            and_(
                Opportunity.assigned_user_id == current_user.id,
                Opportunity.stage == stage
            )
        ).scalar() or 0

        funnel_data.append({
            "stage": stage,
            "count": count,
            "value": float(value)
        })

    return funnel_data

@router.get("/revenue-chart")
def get_revenue_chart(
    months: int = 12,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get revenue data for chart (last N months)"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months*30)

    # Get client IDs for the user's company
    client_ids = [c.id for c in db.query(Client).filter(Client.company_id == current_user.company_id).all()]

    revenue_data = db.query(
        extract('year', Invoice.created_at).label('year'),
        extract('month', Invoice.created_at).label('month'),
        func.sum(Invoice.amount).label('revenue')
    ).filter(
        and_(
            Invoice.client_id.in_(client_ids),
            Invoice.status == 'paid',
            Invoice.created_at >= start_date,
            Invoice.created_at <= end_date
        )
    ).group_by(
        extract('year', Invoice.created_at),
        extract('month', Invoice.created_at)
    ).order_by(
        extract('year', Invoice.created_at),
        extract('month', Invoice.created_at)
    ).all()

    chart_data = []
    for row in revenue_data:
        chart_data.append({
            "month": f"{int(row.year)}-{int(row.month):02d}",
            "revenue": float(row.revenue)
        })

    return chart_data

@router.get("/recent-activity")
def get_recent_activity(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent activity feed"""
    # Recent opportunities
    recent_opportunities = db.query(Opportunity).filter(
        Opportunity.assigned_user_id == current_user.id
    ).order_by(Opportunity.id.desc()).limit(limit).all()

    # Recent clients
    recent_clients = db.query(Client).filter(
        Client.company_id == current_user.company_id
    ).order_by(Client.id.desc()).limit(limit).all()

    activities = []

    # Add opportunity activities
    for opp in recent_opportunities:
        activities.append({
            "type": "opportunity",
            "title": f"New opportunity: {opp.name}",
            "description": f"Value: ${opp.value}",
            "date": opp.id,  # Using ID as timestamp since created_at doesn't exist
            "stage": opp.stage
        })

    # Add client activities
    for client in recent_clients:
        activities.append({
            "type": "client",
            "title": f"New client: {client.name}",
            "description": f"Email: {client.email}",
            "date": client.id  # Using ID as timestamp since created_at doesn't exist
        })

    # Sort by date and limit
    activities.sort(key=lambda x: x['date'], reverse=True)
    return activities[:limit]

@router.get("/performance-kpis")
def get_performance_kpis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get performance KPIs"""
    # Conversion rate (won opportunities / total opportunities)
    total_opportunities = db.query(Opportunity).filter(
        Opportunity.assigned_user_id == current_user.id
    ).count()

    won_opportunities = db.query(Opportunity).filter(
        and_(
            Opportunity.assigned_user_id == current_user.id,
            Opportunity.stage == 'Closed Won'
        )
    ).count()

    conversion_rate = (won_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0

    # Average deal size
    avg_deal_size = db.query(func.avg(Opportunity.value)).filter(
        and_(
            Opportunity.assigned_user_id == current_user.id,
            Opportunity.stage == 'Closed Won'
        )
    ).scalar() or 0

    return {
        "conversion_rate": round(conversion_rate, 2),
        "average_deal_size": round(float(avg_deal_size), 2),
        "total_opportunities": total_opportunities,
        "won_opportunities": won_opportunities
    }

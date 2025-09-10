"""
Monitoring Routes
API endpoints for system monitoring and health checks
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ..database_new import get_db
from ..auth import get_current_user
from ..models import User
from ..services.monitoring_service import monitoring_service
from ..services.alert_service import alert_service

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.get(
    "/health",
    summary="Health Check",
    description="""
    Comprehensive health check endpoint for the CRM system.

    Returns the overall health status and detailed information about:
    - System resources (CPU, memory, disk)
    - Database connectivity
    - API performance
    - Business metrics

    **Response codes:**
    - 200: System is healthy
    - 503: System has issues (but still responding)
    """,
    responses={
        200: {
            "description": "System is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2024-01-15T10:30:00",
                        "status": "healthy",
                        "system": {
                            "cpu_usage": 45.2,
                            "memory_usage": 62.1,
                            "disk_usage": 78.5,
                            "status": "healthy"
                        },
                        "database": {"status": "healthy"},
                        "api": {
                            "status": "healthy",
                            "total_calls": 1250,
                            "error_rate": 2.1,
                            "avg_response_time": 0.85
                        },
                        "business": {
                            "status": "healthy",
                            "conversion_rate": 15.3,
                            "total_clients": 450
                        },
                        "uptime": 86400.5,
                        "version": "1.0.0"
                    }
                }
            }
        },
        503: {
            "description": "System has issues",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2024-01-15T10:30:00",
                        "status": "warning",
                        "error": "High CPU usage detected"
                    }
                }
            }
        }
    }
)
def get_health():
    """Get comprehensive system health status"""
    health_data = monitoring_service.get_health_status()

    # Return 503 if status is not healthy
    if health_data.get('status') != 'healthy':
        raise HTTPException(status_code=503, detail=health_data)

    return health_data

@router.get(
    "/metrics/system",
    summary="System Metrics",
    description="""
    Get system performance metrics for monitoring.

    Returns CPU, memory, disk usage, and other system metrics
    collected over the specified time period.

    **Parameters:**
    - hours: Number of hours of historical data (default: 1, max: 24)
    """,
    dependencies=[Depends(get_current_user)]
)
def get_system_metrics(hours: int = Query(1, ge=1, le=24)):
    """Get system performance metrics"""
    try:
        metrics = monitoring_service.get_system_metrics(hours)
        return {
            "metrics": metrics,
            "count": len(metrics),
            "period_hours": hours
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve system metrics: {str(e)}")

@router.get(
    "/metrics/api",
    summary="API Performance Metrics",
    description="""
    Get API performance metrics and statistics.

    Returns response times, error rates, and endpoint usage
    statistics for the specified time period.

    **Parameters:**
    - hours: Number of hours of historical data (default: 1, max: 24)
    """,
    dependencies=[Depends(get_current_user)]
)
def get_api_metrics(hours: int = Query(1, ge=1, le=24)):
    """Get API performance metrics"""
    try:
        metrics = monitoring_service.get_api_metrics(hours)
        return {
            "metrics": metrics,
            "count": len(metrics),
            "period_hours": hours
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve API metrics: {str(e)}")

@router.get(
    "/metrics/business",
    summary="Business Metrics",
    description="""
    Get business performance metrics and KPIs.

    Returns user counts, client metrics, opportunity values,
    invoice statistics, and conversion rates.

    **Parameters:**
    - hours: Number of hours of historical data (default: 24, max: 168)
    """,
    dependencies=[Depends(get_current_user)]
)
def get_business_metrics(hours: int = Query(24, ge=1, le=168)):
    """Get business performance metrics"""
    try:
        metrics = monitoring_service.get_business_metrics(hours)
        return {
            "metrics": metrics,
            "count": len(metrics),
            "period_hours": hours
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve business metrics: {str(e)}")

@router.get(
    "/alerts",
    summary="Active Alerts",
    description="""
    Get current active alerts and notifications.

    Returns all unresolved alerts with their severity levels
    and timestamps.

    **Parameters:**
    - hours: Number of hours to look back for alerts (default: 24)
    """,
    dependencies=[Depends(get_current_user)]
)
def get_alerts(hours: int = Query(24, ge=1, le=168)):
    """Get active alerts"""
    try:
        alerts = monitoring_service.get_alerts(resolved=False, hours=hours)
        return {
            "alerts": alerts,
            "count": len(alerts),
            "period_hours": hours
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve alerts: {str(e)}")

@router.get(
    "/alerts/history",
    summary="Alert History",
    description="""
    Get historical alerts including resolved ones.

    Returns all alerts (both active and resolved) for
    the specified time period.

    **Parameters:**
    - resolved: Include resolved alerts (default: false)
    - hours: Number of hours to look back (default: 168 - 1 week)
    """,
    dependencies=[Depends(get_current_user)]
)
def get_alert_history(
    resolved: bool = Query(False, description="Include resolved alerts"),
    hours: int = Query(168, ge=1, le=720)  # Max 30 days
):
    """Get alert history"""
    try:
        alerts = monitoring_service.get_alerts(resolved=resolved, hours=hours)
        return {
            "alerts": alerts,
            "count": len(alerts),
            "resolved": resolved,
            "period_hours": hours
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve alert history: {str(e)}")

@router.post(
    "/alerts/{alert_id}/resolve",
    summary="Resolve Alert",
    description="""
    Mark an alert as resolved.

    This will stop the alert from appearing in active alerts
    and mark it as resolved in the history.

    **Parameters:**
    - alert_id: The ID of the alert to resolve
    """,
    dependencies=[Depends(get_current_user)]
)
def resolve_alert(alert_id: str):
    """Resolve an alert"""
    try:
        monitoring_service.resolve_alert(alert_id)
        return {"message": f"Alert {alert_id} resolved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resolve alert: {str(e)}")

@router.get(
    "/performance/summary",
    summary="Performance Summary",
    description="""
    Get a comprehensive performance summary.

    Returns aggregated statistics for system performance,
    API response times, error rates, and business metrics
    over the specified period.

    **Parameters:**
    - hours: Number of hours for the summary (default: 24)
    """,
    dependencies=[Depends(get_current_user)]
)
def get_performance_summary(hours: int = Query(24, ge=1, le=168)):
    """Get comprehensive performance summary"""
    try:
        # Get all metrics
        system_metrics = monitoring_service.get_system_metrics(hours)
        api_metrics = monitoring_service.get_api_metrics(hours)
        business_metrics = monitoring_service.get_business_metrics(hours)
        alerts = monitoring_service.get_alerts(resolved=False, hours=hours)

        # Calculate aggregates
        summary = {
            "period_hours": hours,
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "avg_cpu": sum(m['cpu_percent'] for m in system_metrics) / len(system_metrics) if system_metrics else 0,
                "avg_memory": sum(m['memory_percent'] for m in system_metrics) / len(system_metrics) if system_metrics else 0,
                "avg_disk": sum(m['disk_usage_percent'] for m in system_metrics) / len(system_metrics) if system_metrics else 0,
                "samples": len(system_metrics)
            },
            "api": {
                "total_calls": len(api_metrics),
                "avg_response_time": sum(m['response_time'] for m in api_metrics) / len(api_metrics) if api_metrics else 0,
                "error_rate": (sum(1 for m in api_metrics if m['status_code'] >= 400) / len(api_metrics) * 100) if api_metrics else 0,
                "samples": len(api_metrics)
            },
            "business": business_metrics[-1] if business_metrics else {},
            "alerts": {
                "active_count": len(alerts),
                "critical_count": sum(1 for a in alerts if a['severity'] == 'critical'),
                "high_count": sum(1 for a in alerts if a['severity'] == 'high')
            }
        }

        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate performance summary: {str(e)}")

@router.post(
    "/test-alert",
    summary="Test Alert System",
    description="""
    Send a test alert to verify the alerting system is working.

    This will create a test alert and send notifications through
    all configured channels (email, Slack, etc.).

    **Note:** This is for testing purposes only.
    """,
    dependencies=[Depends(get_current_user)]
)
def test_alert():
    """Send a test alert"""
    try:
        from ..services.monitoring_service import Alert
        import time

        test_alert = Alert(
            id=f"test_{int(time.time())}",
            type="test_alert",
            severity="low",
            message="This is a test alert to verify the alerting system",
            value="test_value",
            threshold="test_threshold",
            timestamp=datetime.utcnow()
        )

        success = alert_service.send_alert(test_alert)

        return {
            "message": "Test alert sent successfully" if success else "Failed to send test alert",
            "success": success
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send test alert: {str(e)}")

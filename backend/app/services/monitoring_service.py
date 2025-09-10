"""
Production Monitoring Service
Comprehensive monitoring and metrics collection for the CRM system
"""
import time
import psutil
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
import os
from dataclasses import dataclass, asdict
from ..utils.performance import PerformanceMonitor
from ..database_new import get_db
from ..models import User, Client, Opportunity, Invoice
from sqlalchemy.orm import Session
from sqlalchemy import func

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    network_connections: int
    active_threads: int
    uptime_seconds: float

@dataclass
class APIMetrics:
    """API performance metrics"""
    endpoint: str
    method: str
    response_time: float
    status_code: int
    timestamp: datetime
    user_id: Optional[int] = None
    ip_address: Optional[str] = None

@dataclass
class BusinessMetrics:
    """Business performance metrics"""
    total_users: int
    active_users_24h: int
    total_clients: int
    total_opportunities: int
    total_opportunities_value: float
    total_invoices: int
    total_invoices_value: float
    paid_invoices_value: float
    conversion_rate: float
    timestamp: datetime

@dataclass
class Alert:
    """Monitoring alert"""
    id: str
    type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    message: str
    value: Any
    threshold: Any
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None

class MonitoringService:
    """Comprehensive monitoring service for production"""

    def __init__(self):
        self.system_metrics = deque(maxlen=1000)  # Keep last 1000 readings
        self.api_metrics = deque(maxlen=5000)     # Keep last 5000 API calls
        self.business_metrics = deque(maxlen=100) # Keep last 100 business readings
        self.alerts = []
        self.alerts_lock = threading.Lock()

        # Alert thresholds
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_usage_percent': 90.0,
            'response_time': 2.0,  # seconds
            'error_rate': 5.0,     # percentage
            'active_users': 1000   # concurrent users
        }

        # Start background monitoring
        self.monitoring_thread = threading.Thread(target=self._background_monitor, daemon=True)
        self.monitoring_thread.start()

        # Performance monitor
        self.performance_monitor = PerformanceMonitor()

    def _background_monitor(self):
        """Background monitoring thread"""
        while True:
            try:
                # Collect system metrics every 30 seconds
                self._collect_system_metrics()

                # Collect business metrics every 5 minutes
                if int(time.time()) % 300 == 0:
                    self._collect_business_metrics()

                # Check for alerts every minute
                if int(time.time()) % 60 == 0:
                    self._check_alerts()

                time.sleep(30)  # Sleep for 30 seconds

            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(60)  # Sleep longer on error

    def _collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            metrics = SystemMetrics(
                timestamp=datetime.utcnow(),
                cpu_percent=psutil.cpu_percent(interval=1),
                memory_percent=psutil.virtual_memory().percent,
                disk_usage_percent=psutil.disk_usage('/').percent,
                network_connections=len(psutil.net_connections()),
                active_threads=threading.active_count(),
                uptime_seconds=time.time() - psutil.boot_time()
            )

            self.system_metrics.append(metrics)

            # Check system alerts
            self._check_system_alerts(metrics)

        except Exception as e:
            print(f"Error collecting system metrics: {e}")

    def _collect_business_metrics(self):
        """Collect business performance metrics"""
        try:
            db = next(get_db())

            # Calculate metrics
            total_users = db.query(func.count(User.id)).scalar() or 0

            # Active users in last 24 hours (users who logged in recently)
            active_cutoff = datetime.utcnow() - timedelta(hours=24)
            active_users = db.query(func.count(User.id)).filter(
                User.created_at >= active_cutoff
            ).scalar() or 0

            total_clients = db.query(func.count(Client.id)).scalar() or 0
            total_opportunities = db.query(func.count(Opportunity.id)).scalar() or 0

            # Sum of opportunity values
            opportunities_value = db.query(func.sum(Opportunity.value)).scalar() or 0.0

            total_invoices = db.query(func.count(Invoice.id)).scalar() or 0
            invoices_value = db.query(func.sum(Invoice.amount)).scalar() or 0.0

            # Paid invoices value
            paid_invoices_value = db.query(func.sum(Invoice.amount)).filter(
                Invoice.status == 'paid'
            ).scalar() or 0.0

            # Conversion rate (paid invoices / total invoices)
            conversion_rate = (total_invoices > 0) and (paid_invoices_value / invoices_value * 100) or 0.0

            metrics = BusinessMetrics(
                total_users=total_users,
                active_users_24h=active_users,
                total_clients=total_clients,
                total_opportunities=total_opportunities,
                total_opportunities_value=float(opportunities_value),
                total_invoices=total_invoices,
                total_invoices_value=float(invoices_value),
                paid_invoices_value=float(paid_invoices_value),
                conversion_rate=float(conversion_rate),
                timestamp=datetime.utcnow()
            )

            self.business_metrics.append(metrics)

        except Exception as e:
            print(f"Error collecting business metrics: {e}")
        finally:
            db.close()

    def record_api_call(self, endpoint: str, method: str, response_time: float,
                       status_code: int, user_id: Optional[int] = None,
                       ip_address: Optional[str] = None):
        """Record API call metrics"""
        metrics = APIMetrics(
            endpoint=endpoint,
            method=method,
            response_time=response_time,
            status_code=status_code,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            ip_address=ip_address
        )

        self.api_metrics.append(metrics)

        # Check API alerts
        self._check_api_alerts(metrics)

    def _check_system_alerts(self, metrics: SystemMetrics):
        """Check for system-related alerts"""
        alerts_to_check = [
            ('cpu_percent', metrics.cpu_percent, 'high', 'CPU usage is high'),
            ('memory_percent', metrics.memory_percent, 'high', 'Memory usage is high'),
            ('disk_usage_percent', metrics.disk_usage_percent, 'critical', 'Disk usage is critical')
        ]

        for metric_name, value, severity, message in alerts_to_check:
            threshold = self.thresholds.get(metric_name)
            if threshold and value > threshold:
                self._create_alert(
                    type=f'system_{metric_name}',
                    severity=severity,
                    message=f"{message}: {value:.1f}% (threshold: {threshold}%)",
                    value=value,
                    threshold=threshold
                )

    def _check_api_alerts(self, metrics: APIMetrics):
        """Check for API-related alerts"""
        # Check response time
        if metrics.response_time > self.thresholds['response_time']:
            self._create_alert(
                type='api_response_time',
                severity='medium',
                message=f"Slow API response: {metrics.endpoint} took {metrics.response_time:.2f}s",
                value=metrics.response_time,
                threshold=self.thresholds['response_time']
            )

        # Check error rate (simplified - in production you'd track over time)
        if metrics.status_code >= 500:
            self._create_alert(
                type='api_error',
                severity='high',
                message=f"API Error: {metrics.endpoint} returned {metrics.status_code}",
                value=metrics.status_code,
                threshold=500
            )

    def _check_alerts(self):
        """Check for various alerts periodically"""
        # Check API error rate over last hour
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_calls = [m for m in self.api_metrics if m.timestamp > one_hour_ago]

        if recent_calls:
            error_count = sum(1 for m in recent_calls if m.status_code >= 400)
            error_rate = (error_count / len(recent_calls)) * 100

            if error_rate > self.thresholds['error_rate']:
                self._create_alert(
                    type='api_error_rate',
                    severity='high',
                    message=f"High API error rate: {error_rate:.1f}% (threshold: {self.thresholds['error_rate']}%)",
                    value=error_rate,
                    threshold=self.thresholds['error_rate']
                )

    def _create_alert(self, type: str, severity: str, message: str,
                     value: Any, threshold: Any):
        """Create a new alert"""
        alert = Alert(
            id=f"{type}_{int(time.time())}",
            type=type,
            severity=severity,
            message=message,
            value=value,
            threshold=threshold,
            timestamp=datetime.utcnow()
        )

        with self.alerts_lock:
            self.alerts.append(alert)

        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]

        print(f"🚨 ALERT [{severity.upper()}]: {message}")

    def get_system_metrics(self, hours: int = 1) -> List[Dict[str, Any]]:
        """Get system metrics for the last N hours"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return [asdict(m) for m in self.system_metrics if m.timestamp > cutoff]

    def get_api_metrics(self, hours: int = 1) -> List[Dict[str, Any]]:
        """Get API metrics for the last N hours"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return [asdict(m) for m in self.api_metrics if m.timestamp > cutoff]

    def get_business_metrics(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get business metrics for the last N hours"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return [asdict(m) for m in self.business_metrics if m.timestamp > cutoff]

    def get_alerts(self, resolved: bool = False, hours: int = 24) -> List[Dict[str, Any]]:
        """Get alerts"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        with self.alerts_lock:
            alerts = [asdict(a) for a in self.alerts
                     if a.timestamp > cutoff and a.resolved == resolved]
        return alerts

    def resolve_alert(self, alert_id: str):
        """Resolve an alert"""
        with self.alerts_lock:
            for alert in self.alerts:
                if alert.id == alert_id and not alert.resolved:
                    alert.resolved = True
                    alert.resolved_at = datetime.utcnow()
                    break

    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        try:
            # System health
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent

            system_health = {
                'cpu_usage': cpu_percent,
                'memory_usage': memory_percent,
                'disk_usage': disk_percent,
                'status': 'healthy' if all(x < 90 for x in [cpu_percent, memory_percent, disk_percent]) else 'warning'
            }

            # Database health
            db_status = 'unknown'
            try:
                db = next(get_db())
                db.execute("SELECT 1")
                db_status = 'healthy'
                db.close()
            except:
                db_status = 'unhealthy'

            # API health (based on recent metrics)
            api_health = self._get_api_health()

            # Business health
            business_health = self._get_business_health()

            return {
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'healthy' if all(h['status'] == 'healthy'
                                         for h in [system_health, {'status': db_status}, api_health, business_health])
                        else 'warning',
                'system': system_health,
                'database': {'status': db_status},
                'api': api_health,
                'business': business_health,
                'uptime': time.time() - psutil.boot_time(),
                'version': os.getenv('APP_VERSION', '1.0.0')
            }

        except Exception as e:
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'error',
                'error': str(e)
            }

    def _get_api_health(self) -> Dict[str, Any]:
        """Get API health status"""
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_calls = [m for m in self.api_metrics if m.timestamp > one_hour_ago]

        if not recent_calls:
            return {'status': 'unknown', 'message': 'No recent API calls'}

        error_count = sum(1 for m in recent_calls if m.status_code >= 400)
        error_rate = (error_count / len(recent_calls)) * 100

        avg_response_time = sum(m.response_time for m in recent_calls) / len(recent_calls)

        status = 'healthy'
        if error_rate > 5 or avg_response_time > 2:
            status = 'warning'
        if error_rate > 10 or avg_response_time > 5:
            status = 'unhealthy'

        return {
            'status': status,
            'total_calls': len(recent_calls),
            'error_rate': error_rate,
            'avg_response_time': avg_response_time
        }

    def _get_business_health(self) -> Dict[str, Any]:
        """Get business health status"""
        if not self.business_metrics:
            return {'status': 'unknown', 'message': 'No business metrics available'}

        latest = self.business_metrics[-1]

        # Simple business health indicators
        health_indicators = []

        if latest.total_users > 0:
            health_indicators.append('has_users')
        if latest.total_clients > 0:
            health_indicators.append('has_clients')
        if latest.conversion_rate > 10:  # 10% conversion rate
            health_indicators.append('good_conversion')

        status = 'healthy' if len(health_indicators) >= 2 else 'warning'

        return {
            'status': status,
            'indicators': health_indicators,
            'conversion_rate': latest.conversion_rate,
            'total_clients': latest.total_clients
        }

# Global monitoring service instance
monitoring_service = MonitoringService()

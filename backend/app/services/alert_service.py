"""
Alert Service
Handles alert notifications via email, Slack, and other channels
"""
import smtplib
import json
import requests
from email.message import EmailMessage
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
from ..utils_functions import enviar_email
from .monitoring_service import Alert

class AlertService:
    """Service for handling alert notifications"""

    def __init__(self):
        self.email_enabled = bool(os.getenv('ALERT_EMAIL_ENABLED', 'true').lower() == 'true')
        self.slack_enabled = bool(os.getenv('ALERT_SLACK_ENABLED', 'false').lower() == 'true')
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')

        # Alert templates
        self.templates = {
            'email': {
                'subject': '🚨 CRM Alert: {alert_type}',
                'body': """
CRM System Alert

Type: {alert_type}
Severity: {severity}
Message: {message}
Value: {value}
Threshold: {threshold}
Time: {timestamp}

Please check the system monitoring dashboard for more details.

Best regards,
CRM Monitoring System
                """
            },
            'slack': {
                'text': '🚨 *CRM Alert*\n\n*Type:* {alert_type}\n*Severity:* {severity}\n*Message:* {message}\n*Value:* {value}\n*Threshold:* {threshold}\n*Time:* {timestamp}',
                'color': {
                    'low': 'good',
                    'medium': 'warning',
                    'high': 'danger',
                    'critical': 'danger'
                }
            }
        }

    def send_alert(self, alert: Alert) -> bool:
        """Send alert through configured channels"""
        success = True

        # Send email alert
        if self.email_enabled:
            if not self._send_email_alert(alert):
                success = False

        # Send Slack alert
        if self.slack_enabled and self.slack_webhook_url:
            if not self._send_slack_alert(alert):
                success = False

        return success

    def _send_email_alert(self, alert: Alert) -> bool:
        """Send alert via email"""
        try:
            subject = self.templates['email']['subject'].format(
                alert_type=alert.type.replace('_', ' ').title()
            )

            body = self.templates['email']['body'].format(
                alert_type=alert.type.replace('_', ' ').title(),
                severity=alert.severity.upper(),
                message=alert.message,
                value=alert.value,
                threshold=alert.threshold,
                timestamp=alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')
            )

            # Get admin email from environment
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@crm.com')

            return enviar_email(admin_email, subject, body.strip())

        except Exception as e:
            print(f"Error sending email alert: {e}")
            return False

    def _send_slack_alert(self, alert: Alert) -> bool:
        """Send alert via Slack webhook"""
        try:
            payload = {
                'text': self.templates['slack']['text'].format(
                    alert_type=alert.type.replace('_', ' ').title(),
                    severity=alert.severity.upper(),
                    message=alert.message,
                    value=alert.value,
                    threshold=alert.threshold,
                    timestamp=alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')
                ),
                'attachments': [{
                    'color': self.templates['slack']['color'].get(alert.severity, 'warning'),
                    'fields': [
                        {
                            'title': 'Alert Type',
                            'value': alert.type.replace('_', ' ').title(),
                            'short': True
                        },
                        {
                            'title': 'Severity',
                            'value': alert.severity.upper(),
                            'short': True
                        }
                    ]
                }]
            }

            response = requests.post(
                self.slack_webhook_url,
                json=payload,
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:
            print(f"Error sending Slack alert: {e}")
            return False

    def send_health_report(self, health_data: Dict[str, Any]) -> bool:
        """Send daily health report"""
        try:
            subject = f"📊 CRM Daily Health Report - {datetime.utcnow().strftime('%Y-%m-%d')}"

            body = f"""
CRM System Health Report

Status: {health_data.get('status', 'unknown').upper()}
Timestamp: {health_data.get('timestamp', 'unknown')}

System Health:
- CPU Usage: {health_data.get('system', {}).get('cpu_usage', 'N/A')}%
- Memory Usage: {health_data.get('system', {}).get('memory_usage', 'N/A')}%
- Disk Usage: {health_data.get('system', {}).get('disk_usage', 'N/A')}%

Database: {health_data.get('database', {}).get('status', 'unknown').upper()}
API Health: {health_data.get('api', {}).get('status', 'unknown').upper()}
Business Health: {health_data.get('business', {}).get('status', 'unknown').upper()}

Uptime: {health_data.get('uptime', 0) / 3600:.1f} hours
Version: {health_data.get('version', 'unknown')}

This is an automated daily health report.
            """

            admin_email = os.getenv('ADMIN_EMAIL', 'admin@crm.com')
            return enviar_email(admin_email, subject, body.strip())

        except Exception as e:
            print(f"Error sending health report: {e}")
            return False

    def send_weekly_summary(self, metrics_data: Dict[str, Any]) -> bool:
        """Send weekly performance summary"""
        try:
            subject = f"📈 CRM Weekly Performance Summary - {datetime.utcnow().strftime('%Y-%m-%d')}"

            body = f"""
CRM System Weekly Performance Summary

Business Metrics:
- Total Users: {metrics_data.get('total_users', 0)}
- Active Users (24h): {metrics_data.get('active_users_24h', 0)}
- Total Clients: {metrics_data.get('total_clients', 0)}
- Total Opportunities: {metrics_data.get('total_opportunities', 0)}
- Opportunities Value: ${metrics_data.get('total_opportunities_value', 0):,.2f}
- Total Invoices: {metrics_data.get('total_invoices', 0)}
- Invoices Value: ${metrics_data.get('total_invoices_value', 0):,.2f}
- Paid Invoices Value: ${metrics_data.get('paid_invoices_value', 0):,.2f}
- Conversion Rate: {metrics_data.get('conversion_rate', 0):.1f}%

System Performance:
- Average CPU Usage: {metrics_data.get('avg_cpu', 0):.1f}%
- Average Memory Usage: {metrics_data.get('avg_memory', 0):.1f}%
- Average Response Time: {metrics_data.get('avg_response_time', 0):.2f}s
- Error Rate: {metrics_data.get('error_rate', 0):.1f}%

This is an automated weekly performance summary.
            """

            admin_email = os.getenv('ADMIN_EMAIL', 'admin@crm.com')
            return enviar_email(admin_email, subject, body.strip())

        except Exception as e:
            print(f"Error sending weekly summary: {e}")
            return False

# Global alert service instance
alert_service = AlertService()

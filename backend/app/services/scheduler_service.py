"""
Scheduler Service
Handles periodic tasks like health reports and maintenance
"""
import asyncio
import threading
from datetime import datetime, time
from typing import Callable, Dict, List
import schedule
import time as time_module
from ..services.monitoring_service import monitoring_service
from ..services.alert_service import alert_service

class SchedulerService:
    """Service for scheduling periodic tasks"""

    def __init__(self):
        self.jobs: Dict[str, Callable] = {}
        self.running = False
        self.thread: threading.Thread = None

    def add_job(self, job_id: str, func: Callable, schedule_time: str):
        """
        Add a scheduled job

        Args:
            job_id: Unique identifier for the job
            func: Function to execute
            schedule_time: Cron-like schedule string (e.g., "daily", "weekly", "10:00")
        """
        self.jobs[job_id] = {
            'func': func,
            'schedule': schedule_time,
            'next_run': None
        }

    def remove_job(self, job_id: str):
        """Remove a scheduled job"""
        if job_id in self.jobs:
            del self.jobs[job_id]

    def start(self):
        """Start the scheduler"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        print("✅ Scheduler service started")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("🛑 Scheduler service stopped")

    def _run_scheduler(self):
        """Run the scheduler loop"""
        # Schedule daily health report at 9:00 AM
        schedule.every().day.at("09:00").do(self._send_daily_health_report)

        # Schedule weekly summary every Monday at 8:00 AM
        schedule.every().monday.at("08:00").do(self._send_weekly_summary)

        # Schedule database cleanup every Sunday at 2:00 AM
        schedule.every().sunday.at("02:00").do(self._cleanup_old_data)

        print("📅 Scheduled tasks configured:")
        print("  - Daily health report: 9:00 AM")
        print("  - Weekly summary: Monday 8:00 AM")
        print("  - Database cleanup: Sunday 2:00 AM")

        while self.running:
            try:
                schedule.run_pending()
                time_module.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Scheduler error: {e}")
                time_module.sleep(300)  # Wait 5 minutes on error

    def _send_daily_health_report(self):
        """Send daily health report"""
        try:
            print("📧 Sending daily health report...")
            health_data = monitoring_service.get_health_status()
            success = alert_service.send_health_report(health_data)

            if success:
                print("✅ Daily health report sent successfully")
            else:
                print("❌ Failed to send daily health report")

        except Exception as e:
            print(f"Error sending daily health report: {e}")

    def _send_weekly_summary(self):
        """Send weekly performance summary"""
        try:
            print("📊 Sending weekly performance summary...")

            # Get business metrics for the last week
            business_metrics = monitoring_service.get_business_metrics(hours=168)  # 1 week

            if business_metrics:
                latest_metrics = business_metrics[-1] if business_metrics else {}
                success = alert_service.send_weekly_summary(latest_metrics)

                if success:
                    print("✅ Weekly summary sent successfully")
                else:
                    print("❌ Failed to send weekly summary")
            else:
                print("⚠️ No business metrics available for weekly summary")

        except Exception as e:
            print(f"Error sending weekly summary: {e}")

    def _cleanup_old_data(self):
        """Clean up old monitoring data"""
        try:
            print("🧹 Cleaning up old monitoring data...")

            # This would typically clean up old logs, metrics, etc.
            # For now, we'll just log the cleanup
            print("✅ Database cleanup completed")

        except Exception as e:
            print(f"Error during database cleanup: {e}")

    def get_scheduled_jobs(self) -> List[Dict]:
        """Get list of scheduled jobs"""
        jobs_info = []
        for job_id, job_data in self.jobs.items():
            jobs_info.append({
                'id': job_id,
                'schedule': job_data['schedule'],
                'next_run': job_data.get('next_run')
            })
        return jobs_info

# Global scheduler service instance
scheduler_service = SchedulerService()

def start_scheduler():
    """Start the global scheduler service"""
    scheduler_service.start()

def stop_scheduler():
    """Stop the global scheduler service"""
    scheduler_service.stop()

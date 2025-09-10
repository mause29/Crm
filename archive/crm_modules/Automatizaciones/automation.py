from datetime import datetime, timedelta

def send_followup_email(user, email_service):
    # email_service.send_email(to=user.email, subject="Follow-up", body="...")
    print(f"Email sent to {user}")

def schedule_reminder(tasks, email_service):
    now = datetime.now()
    for task in tasks:
        if task.due_date - now < timedelta(days=1):
            send_followup_email(task.user, email_service)

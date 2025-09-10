# apps/notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from apps.users.models import User

@shared_task
def notify_task_due(task_id, task_name, user_email):
    send_mail(
        subject=f'Tarea pendiente: {task_name}',
        message=f'Tienes una tarea pendiente con ID {task_id}',
        from_email='no-reply@crm.com',
        recipient_list=[user_email],
        fail_silently=False,
    )

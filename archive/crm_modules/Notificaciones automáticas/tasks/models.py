from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from apps.notifications.tasks import notify_task_due

@receiver(post_save, sender=Task)
def send_task_notification(sender, instance, created, **kwargs):
    if instance.status == 'pending':
        notify_task_due.delay(instance.id, instance.title, instance.assigned_to.email)

# apps/automation/tasks.py
from celery import shared_task
from apps.users.models import User
from apps.opportunities.models import Opportunity
from django.core.mail import send_mail

@shared_task
def weekly_opportunities_summary():
    users = User.objects.all()
    for user in users:
        open_ops = Opportunity.objects.filter(status='open', assigned_to=user)
        send_mail(
            subject='Resumen semanal de oportunidades',
            message=f'Tienes {open_ops.count()} oportunidades abiertas.',
            from_email='no-reply@crm.com',
            recipient_list=[user.email],
            fail_silently=False
        )

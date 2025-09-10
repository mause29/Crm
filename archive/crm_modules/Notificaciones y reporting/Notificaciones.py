from django.core.mail import send_mail

def send_notification_email(subject, body, recipient):
    send_mail(subject, body, "noreply@micrm.com", [recipient])

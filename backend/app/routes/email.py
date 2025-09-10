from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from ..database_new import get_db
from ..models import User, Client, Opportunity
from ..auth import get_current_user

router = APIRouter()

class EmailTemplate(BaseModel):
    name: str
    subject: str
    body: str
    category: str  # welcome, follow_up, proposal, etc.

class SendEmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    template_id: Optional[int] = None

class BulkEmailRequest(BaseModel):
    client_ids: List[int]
    subject: str
    body: str
    template_id: Optional[int] = None

# Email configuration (you would typically store this in environment variables)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

def send_email_background(to_email: str, subject: str, body: str):
    """Background task to send email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, to_email, text)
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")

@router.post("/send")
async def send_email(
    request: SendEmailRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Send a single email"""
    background_tasks.add_task(send_email_background, request.to_email, request.subject, request.body)
    return {"message": "Email queued for sending"}

@router.post("/send-bulk")
async def send_bulk_email(
    request: BulkEmailRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send bulk emails to multiple clients"""
    clients = db.query(Client).filter(Client.id.in_(request.client_ids)).all()

    for client in clients:
        if client.email:
            background_tasks.add_task(
                send_email_background,
                client.email,
                request.subject,
                request.body.replace("{{client_name}}", client.name)
            )

    return {"message": f"Emails queued for {len(clients)} clients"}

@router.get("/templates")
async def get_email_templates(
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get email templates"""
    templates = [
        {
            "id": 1,
            "name": "Welcome Email",
            "subject": "Welcome to Our Services!",
            "body": """
            <h2>Welcome {{client_name}}!</h2>
            <p>Thank you for choosing our services. We're excited to work with you!</p>
            <p>Here's what you can expect from us:</p>
            <ul>
                <li>Dedicated support team</li>
                <li>Regular updates on your projects</li>
                <li>Quality service delivery</li>
            </ul>
            <p>Best regards,<br>Your CRM Team</p>
            """,
            "category": "welcome"
        },
        {
            "id": 2,
            "name": "Follow-up Email",
            "subject": "Following up on our conversation",
            "body": """
            <h2>Hello {{client_name}},</h2>
            <p>I hope this email finds you well. I wanted to follow up on our recent conversation about your needs.</p>
            <p>We're ready to discuss how we can help you achieve your goals. Would you be available for a quick call this week?</p>
            <p>Looking forward to hearing from you!</p>
            <p>Best regards,<br>Your Sales Team</p>
            """,
            "category": "follow_up"
        },
        {
            "id": 3,
            "name": "Proposal Email",
            "subject": "Proposal for {{service_name}}",
            "body": """
            <h2>Proposal for {{client_name}}</h2>
            <p>Thank you for considering our services. Attached is our detailed proposal outlining how we can help you.</p>
            <p>Key highlights:</p>
            <ul>
                <li>Customized solution for your needs</li>
                <li>Competitive pricing</li>
                <li>Fast implementation</li>
                <li>Ongoing support</li>
            </ul>
            <p>Please review the proposal and let us know if you have any questions.</p>
            <p>Best regards,<br>Your Account Manager</p>
            """,
            "category": "proposal"
        }
    ]

    if category:
        templates = [t for t in templates if t["category"] == category]

    return templates

@router.get("/clients")
async def get_clients_for_email(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get clients with email addresses for bulk emailing"""
    clients = db.query(Client).filter(Client.email.isnot(None)).all()
    return [
        {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "company": client.company
        }
        for client in clients
    ]

@router.get("/history")
async def get_email_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """Get email sending history (mock data for now)"""
    # In a real implementation, you'd store email history in the database
    return [
        {
            "id": 1,
            "to_email": "client@example.com",
            "subject": "Welcome Email",
            "sent_at": "2024-01-15T10:30:00Z",
            "status": "sent"
        },
        {
            "id": 2,
            "to_email": "prospect@example.com",
            "subject": "Follow-up",
            "sent_at": "2024-01-14T14:20:00Z",
            "status": "sent"
        }
    ]

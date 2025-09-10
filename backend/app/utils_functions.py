import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import Session
from .database_new import SessionLocal
from .models import LogAuditoria

def log_accion(usuario: str, accion: str, db: Session = None):
    """Log user actions for auditing purposes"""
    if db is None:
        db = SessionLocal()
    try:
        log = LogAuditoria(usuario=usuario, accion=accion)
        db.add(log)
        db.commit()
    except Exception as e:
        print(f"Error logging action: {e}")
        db.rollback()
    finally:
        if db is not SessionLocal():
            db.close()

def enviar_email(to_email: str, subject: str, body: str):
    """
    Send email notification using configured SMTP server.

    This function uses environment variables for SMTP configuration
    to ensure secure email delivery with proper authentication.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        body: Email body content

    Returns:
        bool: True if email sent successfully, False otherwise

    Environment Variables Required:
        EMAIL_SMTP_SERVER: SMTP server hostname (e.g., smtp.gmail.com)
        EMAIL_SMTP_PORT: SMTP server port (e.g., 587 for TLS)
        EMAIL_USERNAME: SMTP authentication username
        EMAIL_PASSWORD: SMTP authentication password
        EMAIL_USE_TLS: Whether to use TLS encryption (True/False)
        EMAIL_FROM: Sender email address (optional, defaults to EMAIL_USERNAME)
    """
    import os

    # Get SMTP configuration from environment variables
    smtp_server = os.getenv("EMAIL_SMTP_SERVER", "localhost")
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    smtp_username = os.getenv("EMAIL_USERNAME")
    smtp_password = os.getenv("EMAIL_PASSWORD")
    use_tls = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
    from_email = os.getenv("EMAIL_FROM", smtp_username or "crm@noreply.com")

    # Validate required configuration
    if not smtp_username or not smtp_password:
        print("Error: EMAIL_USERNAME and EMAIL_PASSWORD environment variables are required")
        return False

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        # Connect to SMTP server
        if use_tls:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
        else:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        # Authenticate
        server.login(smtp_username, smtp_password)

        # Send email
        server.send_message(msg)
        server.quit()

        print(f"Email sent successfully to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"SMTP Connection Error: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error sending email: {e}")
        return False

def validate_email_format(email: str) -> bool:
    """
    Validate email format using regular expression.

    Args:
        email: Email string to validate

    Returns:
        bool: True if email format is valid, False otherwise

    Pattern explanation:
    ^[a-zA-Z0-9._%+-]+  - Local part: alphanumeric, dots, underscores, percent, plus, hyphen
    @[a-zA-Z0-9.-]+     - Domain: alphanumeric, dots, hyphens
    \.                  - Literal dot
    [a-zA-Z]{2,}       - TLD: at least 2 letters
    $
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_phone_number(phone: str) -> str:
    """
    Format and standardize phone number for consistency.

    Args:
        phone: Raw phone number string

    Returns:
        str: Formatted phone number with country code

    Processing:
    1. Remove all non-digit characters except '+'
    2. Add default country code (+1 for US) if not present
    """
    # Remove all non-digit characters except +
    cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')

    # Add default country code if not present
    if not cleaned.startswith('+'):
        cleaned = '+1' + cleaned  # Default to US country code

    return cleaned

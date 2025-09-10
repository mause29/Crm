# Guía de Seguridad - CRM Completo

## 🔒 Introducción

Esta guía detalla las medidas de seguridad implementadas en el sistema CRM y las mejores prácticas para mantener la seguridad del sistema.

## 🛡️ Arquitectura de Seguridad

### Principios de Seguridad

1. **Defensa en Profundidad**: Múltiples capas de protección
2. **Principio de Menor Privilegio**: Acceso mínimo necesario
3. **Fail-Safe Defaults**: Configuración segura por defecto
4. **Zero Trust**: Verificar todo, confiar en nada

### Componentes de Seguridad

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input         │    │   Processing    │    │   Output        │
│   Validation    │───►│   Sanitization  │───►│   Encoding      │
│                 │    │                 │    │                 │
│ - Type checking │    │ - XSS Prevention│    │ - Content-Type  │
│ - Length limits │    │ - SQL Injection │    │ - CORS headers  │
│ - Format validation│  │ - Command injection│  │ - Security headers│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔐 Autenticación y Autorización

### JWT Token Security

```python
# backend/app/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

# Generar clave secreta segura
SECRET_KEY = secrets.token_hex(32)  # 256 bits
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de hash de contraseñas
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)
```

### Implementación de 2FA

```python
# backend/app/auth.py
import pyotp
from cryptography.fernet import Fernet

def generate_2fa_secret():
    """Genera un secreto único para 2FA"""
    return pyotp.random_base32()

def encrypt_secret(secret: str) -> str:
    """Encripta el secreto 2FA antes de almacenarlo"""
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(secret.encode())
    return encrypted.decode()

def verify_2fa_code(secret: str, code: str) -> bool:
    """Verifica el código 2FA"""
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
```

## ✅ Validación y Sanitización de Entradas

### Validación con Pydantic

```python
# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
import re
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(default="user", regex="^(user|manager|admin)$")
    company_id: Optional[int] = None

    @validator('name')
    def validate_name(cls, v):
        # Solo letras, espacios, guiones y apóstrofes
        if not re.match(r"^[a-zA-Z\s\-']+$", v):
            raise ValueError('Name contains invalid characters')
        return v.strip()

    @validator('password')
    def validate_password_strength(cls, v):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
                       v):
            raise ValueError(
                'Password must contain at least one lowercase letter, '
                'one uppercase letter, one number, and one special character'
            )
        return v

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field(..., regex=r'^\+?[\d\s\-\(\)]+$', max_length=20)
    company_id: int
    notes: Optional[str] = Field(None, max_length=1000)

    @validator('phone')
    def validate_phone(cls, v):
        # Normalizar formato de teléfono
        cleaned = re.sub(r'[^\d+]', '', v)
        if not cleaned.startswith('+'):
            cleaned = '+1' + cleaned
        return cleaned
```

### Sanitización de Texto

```python
# backend/app/utils/security.py
import bleach
import html
from typing import Dict, Any

def sanitize_html(text: str) -> str:
    """Sanitiza HTML para prevenir XSS"""
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3']
    allowed_attrs = {}

    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs)

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitiza todas las entradas de texto"""
    sanitized = {}

    for key, value in data.items():
        if isinstance(value, str):
            # Escapar caracteres HTML
            sanitized[key] = html.escape(value.strip())
            # Sanitizar HTML si es necesario
            if key in ['description', 'notes', 'content']:
                sanitized[key] = sanitize_html(value)
        else:
            sanitized[key] = value

    return sanitized

def validate_file_upload(file, allowed_extensions: list, max_size: int = 5*1024*1024):
    """Valida archivos subidos"""
    if not file:
        raise ValueError("No file provided")

    # Verificar extensión
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise ValueError(f"File type not allowed. Allowed: {allowed_extensions}")

    # Verificar tamaño
    file_content = file.file.read()
    if len(file_content) > max_size:
        raise ValueError(f"File too large. Max size: {max_size} bytes")

    # Reset file pointer
    file.file.seek(0)

    return file
```

## 🛡️ Protección contra Ataques Comunes

### SQL Injection Prevention

```python
# backend/app/models.py - Usando SQLAlchemy ORM
from sqlalchemy import text
from sqlalchemy.orm import Session

def get_user_by_email_safe(db: Session, email: str):
    """Consulta segura usando parámetros"""
    # ✅ FORMA SEGURA
    return db.query(User).filter(User.email == email).first()

def get_users_by_role_safe(db: Session, role: str, company_id: int):
    """Consulta con múltiples parámetros"""
    # ✅ FORMA SEGURA
    return db.query(User).filter(
        User.role == role,
        User.company_id == company_id
    ).all()

# ❌ EVITAR: Concatenación de strings
def get_user_by_email_unsafe(db: Session, email: str):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return db.execute(text(query)).fetchone()
```

### XSS (Cross-Site Scripting) Protection

```python
# backend/app/routes/users.py
from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from ..utils.security import sanitize_input

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    # Sanitizar entrada
    user_data = sanitize_input(user.dict())

    # Crear usuario con datos sanitizados
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()

    return UserResponse.from_orm(db_user)

@app.get("/users/{user_id}", response_class=HTMLResponse)
def get_user_profile(user_id: int):
    # Escapar salida HTML
    user_html = f"""
    <div class="user-profile">
        <h1>{html.escape(user.name)}</h1>
        <p>Email: {html.escape(user.email)}</p>
        <p>Role: {html.escape(user.role)}</p>
    </div>
    """
    return HTMLResponse(content=user_html)
```

### CSRF Protection

```python
# backend/app/middleware/csrf.py
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import secrets

class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            # Verificar token CSRF para métodos que modifican datos
            csrf_token = request.headers.get("X-CSRF-Token")
            session_token = request.session.get("csrf_token")

            if not csrf_token or csrf_token != session_token:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="CSRF token missing or incorrect"
                )

        response = await call_next(request)
        return response

# Generar token CSRF
def generate_csrf_token():
    return secrets.token_hex(32)

# En el login endpoint
@app.post("/users/token")
def login(credentials: LoginCredentials, response: Response):
    # ... lógica de autenticación ...

    # Generar y almacenar token CSRF
    csrf_token = generate_csrf_token()
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return {"access_token": token, "csrf_token": csrf_token}
```

### Rate Limiting

```python
# backend/app/middleware/rate_limit.py
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Limpiar requests antiguos
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < 60
        ]

        # Verificar límite
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests"
            )

        # Registrar request
        self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response
```

## 🔒 Configuración de Headers de Seguridad

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)

# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response

app.add_middleware(SecurityHeadersMiddleware)
```

## 🔐 Encriptación de Datos Sensibles

### Encriptación de Contraseñas

```python
# backend/app/auth.py
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000  # Aumentar rounds para mayor seguridad
)

def hash_password(password: str) -> str:
    """Hashea una contraseña"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)
```

### Encriptación de Datos en BD

```python
# backend/app/utils/encryption.py
from cryptography.fernet import Fernet
import os
from base64 import b64encode, b64decode

class DataEncryption:
    def __init__(self):
        # Generar o cargar clave de encriptación
        key_file = "encryption_key.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.key)

        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """Encripta datos sensibles"""
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.cipher.encrypt(data)
        return b64encode(encrypted).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Desencripta datos"""
        try:
            encrypted = b64decode(encrypted_data)
            decrypted = self.cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception:
            raise ValueError("Invalid encrypted data")

# Uso en modelos
encryption = DataEncryption()

class User(Base):
    # ... otros campos ...
    encrypted_ssn = Column(String)  # Número de seguro social encriptado

    def set_ssn(self, ssn: str):
        self.encrypted_ssn = encryption.encrypt(ssn)

    def get_ssn(self) -> str:
        return encryption.decrypt(self.encrypted_ssn)
```

## 📊 Auditoría y Logging

### Sistema de Logs de Seguridad

```python
# backend/app/utils/audit.py
import logging
import json
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import LogAuditoria

# Configurar logger de seguridad
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.INFO)

# Handler para archivo de seguridad
handler = logging.FileHandler("security.log")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
security_logger.addHandler(handler)

def log_security_event(
    event_type: str,
    user_id: Optional[int],
    ip_address: str,
    details: dict,
    db: Session = None
):
    """Registra evento de seguridad"""
    event_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "ip_address": ip_address,
        "details": details
    }

    # Log en archivo
    security_logger.info(json.dumps(event_data))

    # Log en base de datos si está disponible
    if db:
        try:
            log_entry = LogAuditoria(
                usuario=f"user_{user_id}" if user_id else "system",
                accion=f"SECURITY_EVENT: {event_type}",
                detalles=json.dumps(details)
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            security_logger.error(f"Failed to save audit log: {e}")

# Eventos de seguridad comunes
def log_login_attempt(user_email: str, success: bool, ip_address: str, db: Session = None):
    log_security_event(
        "LOGIN_ATTEMPT",
        None,
        ip_address,
        {"email": user_email, "success": success},
        db
    )

def log_failed_login(user_email: str, ip_address: str, db: Session = None):
    log_security_event(
        "FAILED_LOGIN",
        None,
        ip_address,
        {"email": user_email, "reason": "invalid_credentials"},
        db
    )

def log_suspicious_activity(user_id: int, activity: str, ip_address: str, db: Session = None):
    log_security_event(
        "SUSPICIOUS_ACTIVITY",
        user_id,
        ip_address,
        {"activity": activity},
        db
    )
```

### Middleware de Auditoría

```python
# backend/app/middleware/audit.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..utils.audit import log_security_event
from sqlalchemy.orm import Session
from ..database import get_db

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Obtener información de la request
        client_ip = request.client.host
        user_agent = request.headers.get("User-Agent", "")
        path = request.url.path
        method = request.method

        # Obtener usuario si está autenticado
        user_id = getattr(request.state, "user_id", None)

        # Log de la actividad
        await log_security_event(
            "API_ACCESS",
            user_id,
            client_ip,
            {
                "method": method,
                "path": path,
                "user_agent": user_agent
            }
        )

        response = await call_next(request)

        # Log de respuesta si hay error
        if response.status_code >= 400:
            await log_security_event(
                "API_ERROR",
                user_id,
                client_ip,
                {
                    "method": method,
                    "path": path,
                    "status_code": response.status_code
                }
            )

        return response
```

## 🚨 Monitoreo de Seguridad

### Alertas de Seguridad

```python
# backend/app/utils/alerts.py
import smtplib
from email.message import EmailMessage
import os

def send_security_alert(subject: str, message: str, recipients: list = None):
    """Envía alerta de seguridad por email"""
    if not recipients:
        recipients = [os.getenv("SECURITY_ADMIN_EMAIL")]

    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = f"🚨 SECURITY ALERT: {subject}"
    msg["From"] = os.getenv("ALERT_FROM_EMAIL")
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP(os.getenv("EMAIL_SMTP_SERVER")) as server:
            server.starttls()
            server.login(
                os.getenv("EMAIL_USERNAME"),
                os.getenv("EMAIL_PASSWORD")
            )
            server.send_message(msg)
        print(f"Security alert sent: {subject}")
    except Exception as e:
        print(f"Failed to send security alert: {e}")

# Alertas automáticas
def alert_failed_login_attempts(email: str, attempts: int, ip: str):
    """Alerta por múltiples intentos fallidos de login"""
    if attempts >= 5:
        send_security_alert(
            "Multiple Failed Login Attempts",
            f"User {email} has {attempts} failed login attempts from IP {ip}"
        )

def alert_suspicious_activity(user_id: int, activity: str, ip: str):
    """Alerta por actividad sospechosa"""
    send_security_alert(
        "Suspicious Activity Detected",
        f"Suspicious activity '{activity}' detected for user {user_id} from IP {ip}"
    )

def alert_unauthorized_access(path: str, ip: str, user_agent: str):
    """Alerta por acceso no autorizado"""
    send_security_alert(
        "Unauthorized Access Attempt",
        f"Unauthorized access attempt to {path} from IP {ip}\nUser-Agent: {user_agent}"
    )
```

## 🧪 Testing de Seguridad

### Tests de Seguridad Automatizados

```python
# tests/test_security.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sql_injection_protection():
    """Test protección contra SQL injection"""
    # Intento de SQL injection
    response = client.post("/users/", json={
        "name": "'; DROP TABLE users; --",
        "email": "test@example.com",
        "password": "password123"
    })

    # Debería fallar la validación, no ejecutar SQL
    assert response.status_code == 422  # Validation error

def test_xss_protection():
    """Test protección contra XSS"""
    malicious_script = "<script>alert('XSS')</script>"

    response = client.post("/clients/", json={
        "name": malicious_script,
        "email": "test@example.com",
        "phone": "+1234567890",
        "company_id": 1
    })

    assert response.status_code == 200
    data = response.json()

    # El script debería estar sanitizado
    assert "<script>" not in data["name"]
    assert "<script>" in data["name"]  # HTML escaped

def test_rate_limiting():
    """Test rate limiting"""
    # Hacer múltiples requests rápidas
    responses = []
    for _ in range(70):  # Más que el límite
        response = client.get("/health")
        responses.append(response.status_code)

    # Debería haber al menos una respuesta 429 (Too Many Requests)
    assert 429 in responses

def test_csrf_protection():
    """Test protección CSRF"""
    # Request sin token CSRF
    response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })

    # Debería requerir token CSRF
    assert response.status_code in [403, 422]

def test_input_validation():
    """Test validación de entradas"""
    # Email inválido
    response = client.post("/users/", json={
        "name": "Test User",
        "email": "invalid-email",
        "password": "password123"
    })
    assert response.status_code == 422

    # Contraseña demasiado corta
    response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "123"
    })
    assert response.status_code == 422
```

## 📋 Checklist de Seguridad

### Antes del Despliegue
- [ ] ✅ Generar SECRET_KEY segura (256 bits)
- [ ] ✅ Configurar HTTPS en producción
- [ ] ✅ Establecer headers de seguridad
- [ ] ✅ Configurar CORS correctamente
- [ ] ✅ Implementar rate limiting
- [ ] ✅ Validar todas las entradas
- [ ] ✅ Sanitizar salidas HTML
- [ ] ✅ Configurar logging de seguridad
- [ ] ✅ Implementar auditoría
- [ ] ✅ Configurar alertas de seguridad

### Monitoreo Continuo
- [ ] ✅ Monitorear logs de seguridad
- [ ] ✅ Alertas automáticas
- [ ] ✅ Actualizaciones de dependencias
- [ ] ✅ Revisiones de código de seguridad
- [ ] ✅ Tests de penetración regulares

## 📞 Contacto de Seguridad

Para reportar vulnerabilidades de seguridad:
- Email: security@crm-project.com
- PGP Key: [Enlace a clave PGP]
- Política de divulgación: [Enlace a política]

## 📚 Recursos Adicionales

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLAlchemy Security](https://sqlalchemy.org/features.html#security)

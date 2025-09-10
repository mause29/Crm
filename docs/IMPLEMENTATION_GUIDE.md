# Guía de Implementación - CRM Completo

## 📋 Introducción

Esta guía proporciona instrucciones detalladas para implementar, configurar y desplegar el sistema CRM completo.

## 🏗️ Arquitectura Técnica

### Componentes del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Backend     │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (SQLite/PostgreSQL)
│                 │    │                 │    │                 │
│ - Dashboard     │    │ - REST API      │    │ - Users         │
│ - Forms         │    │ - Auth/JWT      │    │ - Clients       │
│ - Analytics     │    │ - Business Logic│    │ - Opportunities │
│ - Real-time     │    │ - PayPal Integration│ - Tasks        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   External      │
                       │   Services      │
                       │                 │
                       │ - PayPal API    │
                       │ - Email Service │
                       │ - ML Services   │
                       └─────────────────┘
```

## 🔧 Configuración del Entorno

### 1. Requisitos del Sistema

#### Backend
- Python 3.8+
- pip (última versión)
- virtualenv

#### Frontend
- Node.js 16+
- npm 7+

#### Base de Datos
- SQLite (desarrollo)
- PostgreSQL 12+ (producción)

#### Servicios Externos
- PayPal Developer Account
- SMTP Server (Gmail, SendGrid, etc.)

### 2. Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Seguridad
SECRET_KEY=your-256-bit-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de Datos
DATABASE_URL=sqlite:///./crm.db
# Para PostgreSQL: postgresql://user:password@localhost/crm_db

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=sandbox  # sandbox o live

# Email
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Aplicación
APP_NAME=CRM Completo
APP_VERSION=1.0.0
DEBUG=True

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 🚀 Despliegue Paso a Paso

### Paso 1: Preparación del Entorno

```bash
# Clonar repositorio
git clone <repository-url>
cd crm-project

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
```

### Paso 2: Configuración del Backend

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de configuración
cp .env.example .env
# Editar .env con valores reales

# Inicializar base de datos
python scripts/init_db.py

# Ejecutar migraciones
alembic upgrade head

# Crear usuario administrador
python scripts/create_admin.py
```

### Paso 3: Configuración del Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.local

# Editar .env.local
REACT_APP_API_URL=http://localhost:8000
REACT_APP_PAYPAL_CLIENT_ID=your-paypal-client-id
```

### Paso 4: Iniciar Servicios

#### Opción A: Desarrollo Local

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

#### Opción B: Usando Docker

```bash
# Construir imágenes
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🔒 Configuración de Seguridad

### 1. Autenticación JWT

```python
# backend/app/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
```

### 2. Validación de Datos

```python
# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
```

### 3. Rate Limiting

```python
# backend/app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
```

### 4. CORS Configuration

```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Configuración de Base de Datos

### SQLite (Desarrollo)

```python
# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./crm.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

### PostgreSQL (Producción)

```python
# backend/app/database.py
DATABASE_URL = "postgresql://user:password@localhost/crm_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)
```

## 💰 Integración PayPal

### 1. Configuración de PayPal

```python
# backend/app/services/paypal_service.py
import paypalrestsdk

paypalrestsdk.configure({
    "mode": os.getenv("PAYPAL_MODE", "sandbox"),
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})
```

### 2. Crear Pago

```python
def create_payment(amount: float, currency: str = "USD"):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": currency
            },
            "description": "Pago de factura CRM"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/success",
            "cancel_url": "http://localhost:3000/payment/cancel"
        }
    })

    if payment.create():
        return payment
    else:
        raise Exception(payment.error)
```

## 📧 Configuración de Email

### 1. Configuración SMTP

```python
# backend/app/services/email_service.py
import smtplib
from email.message import EmailMessage

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_USERNAME")
    msg["To"] = to_email

    with smtplib.SMTP(
        os.getenv("EMAIL_SMTP_SERVER"),
        int(os.getenv("EMAIL_SMTP_PORT"))
    ) as server:
        server.starttls()
        server.login(
            os.getenv("EMAIL_USERNAME"),
            os.getenv("EMAIL_PASSWORD")
        )
        server.send_message(msg)
```

## 🔍 Monitoreo y Logging

### 1. Configuración de Logging

```python
# backend/app/main.py
import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}

dictConfig(LOGGING_CONFIG)
```

### 2. Health Checks

```python
# backend/app/routes/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    return {"status": "healthy"}

@router.get("/db")
def db_health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
```

## 🚀 Optimización para Producción

### 1. Configuración Gunicorn

```bash
# Crear archivo gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
```

### 2. Comando de Inicio

```bash
gunicorn app.main:app -c gunicorn.conf.py
```

### 3. Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/static/files;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🧪 Testing

### 1. Ejecutar Tests

```bash
# Backend
pytest tests/ -v --cov=app --cov-report=html

# Frontend
cd frontend
npm test -- --coverage
```

### 2. Tests de Integración

```python
# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "user_id" in response.json()
```

## 📈 Escalabilidad

### 1. Caché con Redis

```python
# backend/app/cache.py
import redis
from functools import lru_cache

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_data(key: str):
    data = redis_client.get(key)
    return data.decode('utf-8') if data else None

def set_cached_data(key: str, value: str, expire: int = 3600):
    redis_client.setex(key, expire, value)
```

### 2. Background Tasks

```python
# backend/app/tasks.py
from fastapi import BackgroundTasks

def send_notification_email(email: str, message: str):
    # Lógica para enviar email
    pass

@router.post("/send-notification")
def send_notification(
    email: str,
    message: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_notification_email, email, message)
    return {"message": "Notification queued"}
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Error de Conexión a Base de Datos
```bash
# Verificar conexión
python -c "from app.database import engine; print('DB Connected' if engine else 'DB Failed')"
```

#### 2. Error de JWT
```python
# Verificar token
import jwt
token = "your-jwt-token"
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("Token válido:", payload)
except jwt.ExpiredSignatureError:
    print("Token expirado")
except jwt.InvalidTokenError:
    print("Token inválido")
```

#### 3. Error de PayPal
```python
# Verificar configuración PayPal
import paypalrestsdk
print("PayPal configurado:", paypalrestsdk.default().mode)
```

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://sqlalchemy.org/)
- [PayPal Developer](https://developer.paypal.com/)
- [React Documentation](https://reactjs.org/)
- [Docker Documentation](https://docs.docker.com/)

## 📞 Soporte

Para soporte técnico:
- Email: support@crm-project.com
- Documentación: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/your-repo/issues)

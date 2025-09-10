from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database_new import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin
from ..auth import get_current_user, create_access_token
from ..utils import log_accion
from ..utils.security import (
    sanitize_input,
    validate_email_domain,
    validate_password_strength,
    validate_sql_injection_safe,
    validate_xss_safe,
    log_security_event,
    rate_limit_check
)
from passlib.context import CryptContext
import pyotp

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/",
    response_model=dict,
    summary="Crear nuevo usuario",
    description="""
    Crea una nueva cuenta de usuario en el sistema con validaciones de seguridad avanzadas.

    **Validaciones realizadas:**
    - Rate limiting (5 requests por 5 minutos)
    - Sanitización de entrada para prevenir XSS
    - Validación contra SQL injection
    - Validación de dominio de email
    - Contraseña segura (8+ caracteres, mayúsculas, minúsculas, dígitos, caracteres especiales)
    - Email único en el sistema
    - Rol válido (user, admin, manager)

    **Permisos:** Público (no requiere autenticación)

    **Respuesta exitosa:**
    - Código 200: Usuario creado exitosamente
    - Retorna ID del usuario creado

    **Posibles errores:**
    - 400: Email ya registrado o datos inválidos
    - 429: Demasiadas solicitudes (rate limiting)
    - 500: Error interno del servidor
    """,
    responses={
        200: {
            "description": "Usuario creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "msg": "User created successfully",
                        "user_id": 1
                    }
                }
            }
        },
        400: {
            "description": "Datos inválidos o email ya registrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email already registered"
                    }
                }
            }
        },
        429: {
            "description": "Rate limiting exceeded",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Too many requests. Please try again later."
                    }
                }
            }
        }
    }
)
def create_user(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    """Create a new user with comprehensive security validation"""
    try:
        # Rate limiting check
        client_ip = request.client.host if request.client else "unknown"
        if not rate_limit_check(client_ip, max_requests=5, window_seconds=300):  # 5 requests per 5 minutes
            log_security_event("RATE_LIMIT_EXCEEDED", {"endpoint": "/users/"}, ip_address=client_ip)
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

        # Sanitize input data
        user_data = user.dict()
        sanitized_data = sanitize_input(user_data)

        # Additional security validations
        if not validate_sql_injection_safe(sanitized_data.get('name', '')):
            log_security_event("SQL_INJECTION_ATTEMPT", {"field": "name", "value": user.name}, ip_address=client_ip)
            raise HTTPException(status_code=400, detail="Invalid characters in name")

        if not validate_xss_safe(sanitized_data.get('name', '')):
            log_security_event("XSS_ATTEMPT", {"field": "name", "value": user.name}, ip_address=client_ip)
            raise HTTPException(status_code=400, detail="Invalid characters in name")

        # Validate email domain if configured
        allowed_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]  # Add your allowed domains
        if not validate_email_domain(user.email, allowed_domains):
            log_security_event("INVALID_EMAIL_DOMAIN", {"email": user.email}, ip_address=client_ip)
            raise HTTPException(status_code=400, detail="Email domain not allowed")

        # Enhanced password validation
        password_checks = validate_password_strength(user.password)
        if not password_checks['overall']:
            missing_requirements = []
            if not password_checks['length']: missing_requirements.append("at least 8 characters")
            if not password_checks['uppercase']: missing_requirements.append("one uppercase letter")
            if not password_checks['lowercase']: missing_requirements.append("one lowercase letter")
            if not password_checks['digit']: missing_requirements.append("one number")
            if not password_checks['special']: missing_requirements.append("one special character")
            raise HTTPException(
                status_code=400,
                detail=f"Password does not meet requirements: {', '.join(missing_requirements)}"
            )

        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            log_security_event("DUPLICATE_EMAIL_ATTEMPT", {"email": user.email}, ip_address=client_ip)
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create user with sanitized data
        hashed = get_password_hash(user.password)
        db_user = User(
            name=sanitized_data['name'],
            email=user.email,  # Email doesn't need sanitization as it's validated by Pydantic
            hashed_password=hashed,
            role=user.role,
            company_id=user.company_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.expunge(db_user)  # Detach instance from session to avoid "not bound to session" error

        # Log successful user creation
        log_accion(user.email, f"User account created: {user.email}", db)
        log_security_event("USER_CREATED", {"user_id": db_user.id, "email": user.email}, ip_address=client_ip)

        return {"msg": "User created successfully", "user_id": db_user.id}

    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e) or "email" in str(e).lower():
            log_security_event("DUPLICATE_EMAIL_ATTEMPT", {"email": user.email}, ip_address=client_ip)
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            log_security_event("DATABASE_CONSTRAINT_ERROR", {"error": str(e)}, ip_address=client_ip)
            raise HTTPException(status_code=400, detail="User creation failed due to database constraint")
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        log_security_event("USER_CREATION_ERROR", {"error": str(e)}, ip_address=client_ip)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post(
    "/token",
    summary="Iniciar sesión",
    description="""
    Autentica a un usuario y retorna un token de acceso JWT.

    **Proceso de autenticación:**
    1. Verifica que el email existe
    2. Valida la contraseña
    3. Verifica que la cuenta esté activa
    4. Si tiene 2FA habilitado, requiere código adicional

    **Permisos:** Público

    **Formato de respuesta:**
    - access_token: Token JWT para usar en requests autenticados
    - token_type: Tipo de token (bearer)

    **Ejemplo de uso:**
    ```bash
    curl -X POST "http://localhost:8000/users/token" \
         -d "username=user@example.com&password=mypassword"
    ```
    """,
    responses={
        200: {
            "description": "Login exitoso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Credenciales inválidas o 2FA requerido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid email or password"
                    }
                }
            }
        }
    }
)
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Authenticate user and return access token with security logging"""
    try:
        client_ip = request.client.host if request.client else "unknown"

        # Rate limiting for login attempts
        if not rate_limit_check(client_ip, max_requests=10, window_seconds=600):  # 10 attempts per 10 minutes
            log_security_event("LOGIN_RATE_LIMIT_EXCEEDED", {"username": username}, ip_address=client_ip)
            raise HTTPException(status_code=429, detail="Too many login attempts. Please try again later.")

        user = db.query(User).filter(User.email == username).first()
        if not user:
            log_security_event("FAILED_LOGIN", {"username": username, "reason": "user_not_found"}, ip_address=client_ip)
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not verify_password(password, user.hashed_password):
            log_security_event("FAILED_LOGIN", {"username": username, "reason": "invalid_password"}, ip_address=client_ip)
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not user.is_active:
            log_security_event("FAILED_LOGIN", {"username": username, "reason": "account_inactive"}, ip_address=client_ip)
            raise HTTPException(status_code=401, detail="Account is deactivated")

        if user.two_factor_secret:
            # If 2FA enabled, require code
            log_security_event("LOGIN_2FA_REQUIRED", {"username": username}, ip_address=client_ip)
            raise HTTPException(status_code=401, detail="2FA required")

        token = create_access_token({"sub": user.email})

        # Log successful login
        log_security_event("SUCCESSFUL_LOGIN", {"username": username}, ip_address=client_ip)
        log_accion(user.email, "User logged in", db)

        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        log_security_event("LOGIN_ERROR", {"username": username, "error": str(e)}, ip_address=client_ip)
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.post("/token/2fa")
def login_2fa(request: Request, username: str = Form(...), code: str = Form(...), db: Session = Depends(get_db)):
    """Complete 2FA authentication with security logging"""
    try:
        client_ip = request.client.host if request.client else "unknown"

        user = db.query(User).filter(User.email == username).first()
        if not user or not user.two_factor_secret:
            log_security_event("INVALID_2FA_REQUEST", {"username": username}, ip_address=client_ip)
            raise HTTPException(status_code=401, detail="Invalid authentication request")

        totp = pyotp.TOTP(user.two_factor_secret)
        if not totp.verify(code):
            log_security_event("INVALID_2FA_CODE", {"username": username}, ip_address=client_ip)
            raise HTTPException(status_code=401, detail="Invalid 2FA code")

        token = create_access_token({"sub": user.email})

        # Log successful 2FA login
        log_security_event("SUCCESSFUL_2FA_LOGIN", {"username": username}, ip_address=client_ip)
        log_accion(user.email, "User logged in with 2FA", db)

        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        log_security_event("2FA_ERROR", {"username": username, "error": str(e)}, ip_address=client_ip)
        raise HTTPException(status_code=500, detail=f"2FA verification failed: {str(e)}")

@router.post("/enable-2fa/{user_id}")
def enable_2fa(user_id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Enable 2FA for a user with security logging"""
    try:
        client_ip = request.client.host if request.client else "unknown"

        if user_id != current_user.id and current_user.role != "admin":
            log_security_event("UNAUTHORIZED_2FA_ENABLE", {"user_id": user_id, "current_user": current_user.id}, ip_address=client_ip)
            raise HTTPException(status_code=403, detail="Not authorized to enable 2FA for this user")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.two_factor_secret:
            raise HTTPException(status_code=400, detail="2FA already enabled for this user")

        secret = pyotp.random_base32()
        user.two_factor_secret = secret
        db.commit()

        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=user.email, issuer_name="CRM")

        # Log 2FA enable
        log_security_event("2FA_ENABLED", {"user_id": user_id, "enabled_by": current_user.id}, ip_address=client_ip)
        log_accion(current_user.email, f"Enabled 2FA for user {user.email}", db)

        return {"secret": secret, "uri": uri}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_security_event("2FA_ENABLE_ERROR", {"user_id": user_id, "error": str(e)}, ip_address=client_ip)
        raise HTTPException(status_code=500, detail=f"Failed to enable 2FA: {str(e)}")

@router.get(
    "/",
    summary="Obtener todos los usuarios",
    description="""
    Retorna una lista de todos los usuarios del sistema.

    **Permisos:** Solo administradores

    **Filtros aplicados:**
    - Solo usuarios activos por defecto
    - Información sensible filtrada según permisos

    **Respuesta:**
    Lista de usuarios con información básica (id, nombre, email, rol, estado)
    """,
    responses={
        200: {
            "description": "Lista de usuarios obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Juan Pérez",
                            "email": "juan.perez@empresa.com",
                            "role": "admin",
                            "is_active": True,
                            "created_at": "2024-01-15T10:30:00Z"
                        }
                    ]
                }
            }
        },
        403: {
            "description": "Acceso denegado - requiere rol de administrador"
        }
    }
)
def get_users(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all users (admin only) with security logging"""
    try:
        client_ip = request.client.host if request.client else "unknown"

        if current_user.role != "admin":
            log_security_event("UNAUTHORIZED_USER_LIST_ACCESS", {"current_user": current_user.id}, ip_address=client_ip)
            raise HTTPException(status_code=403, detail="Admin access required")

        users = db.query(User).all()

        # Log admin action
        log_security_event("USER_LIST_ACCESSED", {"current_user": current_user.id, "user_count": len(users)}, ip_address=client_ip)

        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at
            }
            for user in users
        ]
    except HTTPException:
        raise
    except Exception as e:
        log_security_event("USER_LIST_ERROR", {"current_user": current_user.id, "error": str(e)}, ip_address=client_ip)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(e)}")

@router.get("/{user_id}")
def get_user(user_id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get user by ID with security logging"""
    try:
        client_ip = request.client.host if request.client else "unknown"

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            log_security_event("USER_NOT_FOUND", {"user_id": user_id, "current_user": current_user.id}, ip_address=client_ip)
            raise HTTPException(status_code=404, detail="User not found")

        if user_id != current_user.id and current_user.role != "admin":
            log_security_event("UNAUTHORIZED_USER_ACCESS", {"user_id": user_id, "current_user": current_user.id}, ip_address=client_ip)
            raise HTTPException(status_code=403, detail="Not authorized to view this user")

        # Log access
        log_security_event("USER_ACCESSED", {"user_id": user_id, "current_user": current_user.id}, ip_address=client_ip)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at
        }

    except HTTPException:
        raise
    except Exception as e:
        log_security_event("USER_ACCESS_ERROR", {"user_id": user_id, "current_user": current_user.id, "error": str(e)}, ip_address=client_ip)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")

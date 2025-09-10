from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ..database_new import get_db
from ..models import Client, User
from ..schemas import ClientCreate
from ..auth import get_current_user
from ..utils import log_accion

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get(
    "/",
    summary="Obtener lista de clientes",
    description="""
    Recupera la lista completa de clientes asociados a la compañía del usuario autenticado.

    **Características:**
    - Solo muestra clientes de la misma compañía
    - Requiere autenticación JWT
    - Ordena por fecha de creación (más recientes primero)

    **Permisos:** Usuario autenticado

    **Respuesta exitosa:**
    - Código 200: Lista de clientes devuelta exitosamente
    - Retorna array de objetos cliente con información básica

    **Posibles errores:**
    - 401: No autorizado (token inválido o faltante)
    - 500: Error interno del servidor
    """,
    responses={
        200: {
            "description": "Lista de clientes obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "María García",
                            "email": "maria.garcia@cliente.com",
                            "phone": "+34 612 345 678",
                            "created_at": "2024-01-15T10:30:00Z"
                        },
                        {
                            "id": 2,
                            "name": "Carlos Rodríguez",
                            "email": "carlos.rodriguez@empresa.com",
                            "phone": "+34 698 765 432",
                            "created_at": "2024-01-10T14:20:00Z"
                        }
                    ]
                }
            }
        },
        401: {
            "description": "No autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        }
    }
)
def get_clients(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clients = db.query(Client).filter(Client.company_id == current_user.company_id).all()
    return [
        {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "created_at": client.created_at
        }
        for client in clients
    ]

@router.post(
    "/",
    summary="Crear nuevo cliente",
    description="""
    Crea un nuevo cliente asociado a la compañía del usuario autenticado.

    **Validaciones:**
    - Email único en la base de datos
    - Requiere autenticación JWT

    **Permisos:** Usuario autenticado

    **Respuesta exitosa:**
    - Código 200: Cliente creado exitosamente
    - Retorna ID del cliente creado

    **Posibles errores:**
    - 400: Email ya registrado o datos inválidos
    - 500: Error interno del servidor
    """,
    responses={
        200: {
            "description": "Cliente creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "msg": "Client created",
                        "client_id": 1
                    }
                }
            }
        },
        400: {
            "description": "Datos inválidos o email ya registrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Client with this email already exists"
                    }
                }
            }
        }
    }
)
def create_client(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_client = db.query(Client).filter(Client.email == email).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Client with this email already exists")

    db_client = Client(
        name=name,
        email=email,
        phone=phone,
        company_id=current_user.company_id,
        created_by=current_user.id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    # Log the action
    log_accion(current_user.email, f"Created client {name}", db)

    # TODO: Send welcome email (function not implemented yet)
    # enviar_email(email, "Welcome to CRM", "You have been registered as a client.")

    return {"msg": "Client created", "client_id": db_client.id}

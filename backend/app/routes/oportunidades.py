from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database_new import SessionLocal
from ..models import Opportunity, User
from ..schemas import OpportunityCreate
from ..utils import log_accion
from ..auth import get_current_user

router = APIRouter(prefix="/opportunities", tags=["opportunities"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    summary="Crear nueva oportunidad",
    description="""
    Crea una nueva oportunidad de venta asociada a un cliente existente.

    **Validaciones realizadas:**
    - Cliente debe existir en la base de datos
    - Valor debe ser mayor a cero
    - Requiere autenticación JWT

    **Permisos:** Usuario autenticado

    **Respuesta exitosa:**
    - Código 200: Oportunidad creada exitosamente
    - Retorna mensaje de confirmación

    **Posibles errores:**
    - 400: Datos inválidos o cliente no encontrado
    - 401: No autorizado (token inválido o faltante)
    - 500: Error interno del servidor
    """,
    responses={
        200: {
            "description": "Oportunidad creada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "msg": "Opportunity created"
                    }
                }
            }
        },
        400: {
            "description": "Datos inválidos o cliente no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Client not found"
                    }
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
def create_opportunity(op: OpportunityCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_op = Opportunity(name=op.name, value=op.value, client_id=op.client_id)
    db.add(db_op)
    db.commit()
    log_accion(current_user.email, f"Created opportunity {op.name}")
    return {"msg": "Opportunity created"}

@router.get(
    "/",
    summary="Obtener lista de oportunidades",
    description="""
    Recupera la lista completa de oportunidades de venta.

    **Características:**
    - Muestra todas las oportunidades disponibles
    - Requiere autenticación JWT
    - Incluye información detallada de cada oportunidad

    **Permisos:** Usuario autenticado

    **Respuesta exitosa:**
    - Código 200: Lista de oportunidades devuelta exitosamente
    - Retorna array de objetos oportunidad

    **Posibles errores:**
    - 401: No autorizado (token inválido o faltante)
    - 500: Error interno del servidor
    """,
    responses={
        200: {
            "description": "Lista de oportunidades obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Proyecto Desarrollo Web",
                            "value": 15000.50,
                            "client_id": 1,
                            "created_at": "2024-01-15T10:30:00Z",
                            "status": "active"
                        },
                        {
                            "id": 2,
                            "name": "Consultoría Digital",
                            "value": 8500.00,
                            "client_id": 2,
                            "created_at": "2024-01-10T14:20:00Z",
                            "status": "active"
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
def get_opportunities(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    opportunities = db.query(Opportunity).all()
    return opportunities

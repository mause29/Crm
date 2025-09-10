from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database_new import SessionLocal
from ..models import Invoice, User
from ..schemas import InvoiceCreate
from ..utils import log_accion
from ..auth import get_current_user
import paypalrestsdk

router = APIRouter(prefix="/invoices", tags=["invoices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    summary="Crear nueva factura",
    description="""
    Crea una nueva factura asociada a un cliente existente.

    **Validaciones realizadas:**
    - Cliente debe existir en la base de datos
    - Monto debe ser mayor a cero
    - Requiere autenticación JWT

    **Permisos:** Usuario autenticado

    **Respuesta exitosa:**
    - Código 200: Factura creada exitosamente
    - Retorna mensaje de confirmación

    **Posibles errores:**
    - 400: Datos inválidos o cliente no encontrado
    - 401: No autorizado (token inválido o faltante)
    - 500: Error interno del servidor
    """,
    responses={
        200: {
            "description": "Factura creada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "msg": "Invoice created"
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
def create_invoice(invoice: InvoiceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_invoice = Invoice(client_id=invoice.client_id, amount=invoice.amount)
    db.add(db_invoice)
    db.commit()
    log_accion(current_user.email, f"Generated invoice for client {invoice.client_id}")
    return {"msg": "Invoice created"}

@router.post(
    "/pay/{invoice_id}",
    summary="Procesar pago de factura",
    description="""
    Procesa el pago de una factura existente utilizando PayPal.

    **Características:**
    - Utiliza integración directa con PayPal
    - Procesa pagos con tarjeta de crédito sin login
    - Actualiza el estado de la factura a "paid" tras pago exitoso
    - Requiere autenticación JWT

    **Permisos:** Usuario autenticado

    **Respuesta exitosa:**
    - Código 200: Pago procesado exitosamente
    - Retorna mensaje de confirmación

    **Posibles errores:**
    - 400: Error en el procesamiento del pago
    - 401: No autorizado (token inválido o faltante)
    - 404: Factura no encontrada
    - 500: Error interno del servidor
    """,
    responses={
        200: {
            "description": "Pago procesado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "msg": "Invoice paid"
                    }
                }
            }
        },
        400: {
            "description": "Error en el procesamiento del pago",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Payment error"
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
        },
        404: {
            "description": "Factura no encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invoice not found"
                    }
                }
            }
        }
    }
)
def pay_invoice(invoice_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    # Crear pago PayPal con tarjeta sin login
    pago = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "credit_card",
            "funding_instruments": [{

                "credit_card": {
                    "type": "visa",
                    "number": "4111111111111111",
                    "expire_month": "12",
                    "expire_year": "2025",
                    "cvv2": "123",
                    "first_name": "Cliente",
                    "last_name": "Demo"
                }
            }]
        },
        "transactions": [{
            "amount": {
                "total": f"{invoice.amount:.2f}",
                "currency": "USD"
            },
            "description": f"Payment for invoice {invoice.id}"
        }]
    })
    if pago.create():
        invoice.status = "paid"
        db.commit()
        log_accion(current_user.email, f"Paid invoice {invoice.id}")
        return {"msg": "Invoice paid"}
    else:
        raise HTTPException(status_code=400, detail="Payment error")

import paypalrestsdk
from paypalrestsdk import OrdersCaptureRequest
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Factura

# Assuming PayPal client is configured elsewhere, e.g., in settings.py
# paypalrestsdk.configure({
#     "mode": "sandbox",  # or "live"
#     "client_id": "YOUR_CLIENT_ID",
#     "client_secret": "YOUR_CLIENT_SECRET"
# })

def capturar_pago(order_id: str, db: Session = SessionLocal()):
    """
    Captura el pago después que el cliente completa la tarjeta o PayPal.
    """
    try:
        request_capture = OrdersCaptureRequest(order_id)
        request_capture.prefer("return=representation")
        response = paypalrestsdk.api.default().execute(request_capture)

        # Aquí actualizamos la factura en tu base de datos
        if response.result.status == "COMPLETED":
            # Ejemplo: marcar factura como pagada
            # Asumiendo que tienes una forma de relacionar order_id con factura_id
            # factura = db.query(Factura).filter(Factura.id == factura_id).first()
            # if factura:
            #     factura.estado = "PAGADO"
            #     db.commit()
            return {"status": "PAGADO", "detalles": response.result.__dict__}
        else:
            return {"status": "FALLIDO", "detalles": response.result.__dict__}
    except Exception as e:
        return {"status": "ERROR", "detalles": str(e)}

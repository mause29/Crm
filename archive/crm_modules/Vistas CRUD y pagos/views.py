from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Factura, Cliente, Oportunidad
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypal_config import client

# --- Crear Factura ---
def crear_factura(request):
    # Ejemplo de creación desde JSON POST
    data = request.POST
    cliente = get_object_or_404(Cliente, id=data.get("cliente_id"))
    oportunidad = get_object_or_404(Oportunidad, id=data.get("oportunidad_id")) if data.get("oportunidad_id") else None
    
    factura = Factura.objects.create(
        cliente=cliente,
        oportunidad=oportunidad,
        monto=data.get("monto"),
    )
    return JsonResponse({"status": "OK", "factura_id": factura.id})

# --- Crear orden PayPal ---
def crear_orden(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    
    request_paypal = OrdersCreateRequest()
    request_paypal.prefer("return=representation")
    request_paypal.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": str(factura.monto)
            },
            "description": f"Factura #{factura.id}"
        }],
        "application_context": {
            "brand_name": "Mi Empresa",
            "landing_page": "BILLING",
            "user_action": "PAY_NOW",
            "shipping_preference": "NO_SHIPPING"
        }
    })

    response = client.execute(request_paypal)
    factura.paypal_order_id = response.result.id
    factura.save()
    return JsonResponse({"paypal_order_id": response.result.id, "links": [link.__dict__ for link in response.result.links]})

# --- Capturar pago ---
def capturar_pago(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    request_capture = OrdersCaptureRequest(factura.paypal_order_id)
    request_capture.prefer("return=representation")
    response = client.execute(request_capture)

    if response.result.status == "COMPLETED":
        factura.estado = "PAGADO"
        factura.save()
        return JsonResponse({"status": "PAGADO", "detalles": response.result.__dict__})
    else:
        return JsonResponse({"status": "FALLIDO", "detalles": response.result.__dict__})

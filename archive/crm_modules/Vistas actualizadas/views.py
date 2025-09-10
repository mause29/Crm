from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Factura, Cliente, Oportunidad
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypal_config import client

# --- Panel de facturas ---
def panel_facturas(request):
    facturas = Factura.objects.all().order_by('-fecha')
    return render(request, 'facturas/panel.html', {"facturas": facturas})

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
    return JsonResponse({"paypal_order_id": response.result.id})

# --- Capturar pago ---
def capturar_pago(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    request_capture = OrdersCaptureRequest(factura.paypal_order_id)
    request_capture.prefer("return=representation")
    response = client.execute(request_capture)

    if response.result.status == "COMPLETED":
        factura.estado = "PAGADO"
        factura.save()
        return JsonResponse({"status": "PAGADO"})
    else:
        return JsonResponse({"status": "FALLIDO"})

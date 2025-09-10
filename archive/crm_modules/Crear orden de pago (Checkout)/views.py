from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from django.http import JsonResponse
from paypal_config import client

def crear_orden(request):
    """
    Crea una orden de PayPal para que el cliente pague con tarjeta o PayPal.
    """
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "50.00"  # Monto de ejemplo, puedes usar variable
                },
                "description": "Factura #1234"
            }
        ],
        "application_context": {
            "brand_name": "Mi Empresa",
            "landing_page": "BILLING",
            "user_action": "PAY_NOW",
            "shipping_preference": "NO_SHIPPING"
        }
    }

    request_paypal = OrdersCreateRequest()
    request_paypal.prefer("return=representation")
    request_paypal.request_body(data)

    response = client.execute(request_paypal)
    return JsonResponse(response.result.__dict__, safe=False)

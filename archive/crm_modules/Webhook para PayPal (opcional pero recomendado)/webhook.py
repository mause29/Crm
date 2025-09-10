from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def webhook_paypal(request):
    evento = json.loads(request.body)
    
    # Aquí puedes validar el evento y actualizar la factura
    if evento['event_type'] == "CHECKOUT.ORDER.APPROVED":
        order_id = evento['resource']['id']
        # Capturar automáticamente o marcar como aprobado
    return JsonResponse({"status": "ok"})

from rest_framework.views import APIView
from rest_framework.response import Response
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from .models import Invoice

# Configuración PayPal
environment = SandboxEnvironment(client_id="TU_CLIENT_ID", client_secret="TU_CLIENT_SECRET")
paypal_client = PayPalHttpClient(environment)

class CreatePaypalOrder(APIView):
    def post(self, request):
        invoice_id = request.data.get("invoice_id")
        invoice = Invoice.objects.get(id=invoice_id)

        request_order = OrdersCreateRequest()
        request_order.prefer('return=representation')
        request_order.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {"currency_code": invoice.currency, "value": str(invoice.amount)}
            }],
            "application_context": {
                "brand_name": "MiCRM",
                "landing_page": "NO_PREFERENCE",
                "user_action": "PAY_NOW",
            }
        })
        response = paypal_client.execute(request_order)
        return Response(response.result.__dict__)

class CapturePaypalOrder(APIView):
    def post(self, request):
        order_id = request.data.get("order_id")
        request_capture = OrdersCaptureRequest(order_id)
        response = paypal_client.execute(request_capture)
        return Response(response.result.__dict__)

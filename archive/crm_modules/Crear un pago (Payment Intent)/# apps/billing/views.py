# apps/billing/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from .paypal_client import PayPalClient

class PayPalCreateOrderView(APIView, PayPalClient):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')  # en formato "10.00"
        request_order = OrdersCreateRequest()
        request_order.prefer('return=representation')
        request_order.request_body(
            {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": "USD",
                        "value": amount
                    }
                }]
            }
        )

        response = self.client.client.execute(request_order)
        return Response({'orderID': response.result.id})

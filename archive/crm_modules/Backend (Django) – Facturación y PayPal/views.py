import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save(status='pending')

        # Crear orden PayPal
        access_token = self.get_paypal_token()
        order = self.create_paypal_order(invoice, access_token)

        return Response({
            'invoice': serializer.data,
            'paypal_order': order
        }, status=status.HTTP_201_CREATED)

    def get_paypal_token(self):
        url = f'https://api-m.{settings.PAYPAL_MODE}.paypal.com/v1/oauth2/token'
        auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
        headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
        data = {'grant_type': 'client_credentials'}
        response = requests.post(url, headers=headers, data=data, auth=auth)
        return response.json()['access_token']

    def create_paypal_order(self, invoice, token):
        url = f'https://api-m.{settings.PAYPAL_MODE}.paypal.com/v2/checkout/orders'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": invoice.currency,
                        "value": str(invoice.amount)
                    },
                    "description": f"Factura para {invoice.client_name}"
                }
            ],
            "application_context": {
                "return_url": "http://localhost:3000/success",
                "cancel_url": "http://localhost:3000/cancel",
                "brand_name": "Mi CRM",
                "landing_page": "BILLING",
                "user_action": "PAY_NOW"
            }
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

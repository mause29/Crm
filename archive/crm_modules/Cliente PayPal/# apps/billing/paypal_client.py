# apps/billing/paypal_client.py
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from django.conf import settings

class PayPalClient:
    def __init__(self):
        if settings.PAYPAL_MODE == "sandbox":
            self.environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID,
                                                  client_secret=settings.PAYPAL_CLIENT_SECRET)
        else:
            self.environment = LiveEnvironment(client_id=settings.PAYPAL_CLIENT_ID,
                                              client_secret=settings.PAYPAL_CLIENT_SECRET)
        self.client = PayPalHttpClient(self.environment)

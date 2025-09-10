import os
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest

CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYPAL_SECRET")

environment = SandboxEnvironment(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
client = PayPalHttpClient(environment)

def create_order(amount: float, currency="USD"):
    request = OrdersCreateRequest()
    request.prefer("return=representation")
    request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": currency, "value": str(amount)}}],
        "application_context": {"return_url": "https://tucrm.com/success", "cancel_url": "https://tucrm.com/cancel"}
    })
    response = client.execute(request)
    return response.result

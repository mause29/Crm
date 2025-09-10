from fastapi import APIRouter, HTTPException
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

router = APIRouter()

client_id = "TU_CLIENT_ID"
client_secret = "TU_SECRET"
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
paypal_client = PayPalHttpClient(environment)

@router.post("/create-order")
async def create_order(amount: float):
    request = OrdersCreateRequest()
    request.prefer("return=representation")
    request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": "USD", "value": str(amount)}}],
        "application_context": {"user_action": "PAY_NOW"}
    })
    response = paypal_client.execute(request)
    return response.result

@router.post("/capture-order/{order_id}")
async def capture_order(order_id: str):
    request = OrdersCaptureRequest(order_id)
    response = paypal_client.execute(request)
    return response.result

import paypalrestsdk
import os

paypalrestsdk.configure({
    "mode": "sandbox",  # "live" en producción
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

def create_payment(amount: float, currency: str = "USD", description: str = "Invoice Payment"):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "credit_card",
            "funding_instruments": [{
                "credit_card": {
                    "type": "visa",
                    "number": "4111111111111111",
                    "expire_month": "12",
                    "expire_year": "2025",
                    "cvv2": "123",
                    "first_name": "Test",
                    "last_name": "User"
                }
            }]
        },
        "transactions": [{
            "amount": {"total": f"{amount:.2f}", "currency": currency},
            "description": description
        }]
    })
    if payment.create():
        return payment.id
    else:
        return None

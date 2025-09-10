import paypalrestsdk
from config import Config

paypalrestsdk.configure({
  "mode": "sandbox",
  "client_id": Config.PAYPAL_CLIENT_ID,
  "client_secret": Config.PAYPAL_CLIENT_SECRET
})

def create_payment(invoice_id, amount):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "credit_card",
            "funding_instruments": [{
                "credit_card": {
                    # Aquí se recibe info de tarjeta del cliente
                }
            }]
        },
        "transactions": [{
            "amount": {
                "total": f"{amount:.2f}",
                "currency": "USD"
            },
            "description": f"Invoice #{invoice_id}"
        }]
    })
    if payment.create():
        return payment.id
    return None

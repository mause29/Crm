import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox", # o live
    "client_id": "TU_CLIENT_ID",
    "client_secret": "TU_CLIENT_SECRET"
})

def create_payment(amount: float, currency="USD", description="Factura"):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {"total": f"{amount:.2f}", "currency": currency},
            "description": description
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute",
            "cancel_url": "http://localhost:8000/payment/cancel"
        }
    })
    if payment.create():
        return payment
    else:
        return payment.error

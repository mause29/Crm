
import stripe

stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

def create_customer(email):
    return stripe.Customer.create(email=email)

def create_payment_intent(customer_id, amount, currency="usd"):
    return stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer_id
    )

def process_paypal_payment(payment_id, token):
    import requests
    url = f"https://api.sandbox.paypal.com/v1/payments/payment/{payment_id}/execute"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(url, headers=headers)
    return r.json()

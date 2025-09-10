from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"

environment = SandboxEnvironment(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
client = PayPalHttpClient(environment)

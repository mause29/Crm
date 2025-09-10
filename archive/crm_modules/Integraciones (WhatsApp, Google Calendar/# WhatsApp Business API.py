# WhatsApp Business API
def send_whatsapp_message(phone, message):
    import requests
    url = "https://graph.facebook.com/v15.0/WHATSAPP_PHONE_ID/messages"
    token = "TU_ACCESS_TOKEN"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": phone, "text": {"body": message}}
    requests.post(url, json=data, headers=headers)

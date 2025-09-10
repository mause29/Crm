import requests
from datetime import datetime

# Google Calendar API (ejemplo básico)
def add_event_to_google_calendar(event_title, start_time, end_time, calendar_id, token):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "summary": event_title,
        "start": {"dateTime": start_time},
        "end": {"dateTime": end_time},
    }
    r = requests.post(url, json=data, headers=headers)
    return r.json()

# WhatsApp Business API
def send_whatsapp_message(phone_number, message, token):
    url = "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    r = requests.post(url, json=data, headers=headers)
    return r.json()

# Telefonía VoIP (Ejemplo con API ficticia)
def make_voip_call(from_number, to_number, token):
    url = "https://api.voipprovider.com/call"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"from": from_number, "to": to_number}
    r = requests.post(url, json=data, headers=headers)
    return r.json()

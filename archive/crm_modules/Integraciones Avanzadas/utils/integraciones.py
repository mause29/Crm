# Google Calendar / Outlook
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import datetime

def crear_evento_google_calendar(creds, resumen, inicio, fin, participantes=[]):
    service = build("calendar", "v3", credentials=creds)
    evento = {
        'summary': resumen,
        'start': {'dateTime': inicio.isoformat(), 'timeZone': 'America/Santo_Domingo'},
        'end': {'dateTime': fin.isoformat(), 'timeZone': 'America/Santo_Domingo'},
        'attendees': [{'email': e} for e in participantes]
    }
    evento = service.events().insert(calendarId='primary', body=evento).execute()
    return evento.get('id')

# WhatsApp Business API
import requests

def enviar_whatsapp(mensaje, telefono, token, phone_number_id):
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {"body": mensaje}
    }
    r = requests.post(url, headers=headers, json=data)
    return r.json()

# VoIP (Ejemplo Asterisk AMI)
from asterisk.ami import AMIClient

def realizar_llamada_voip(host, port, username, secret, extension, numero):
    client = AMIClient(address=host, port=port)
    client.login(username=username, secret=secret)
    client.originate(
        endpoint=f"SIP/{extension}",
        exten=numero,
        context="from-internal",
        priority=1,
        caller_id=extension
    )
    client.logoff()

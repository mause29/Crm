# Google Calendar API
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_calendar_event(summary, start, end):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    event = {'summary': summary, 'start': {'dateTime': start}, 'end': {'dateTime': end}}
    service.events().insert(calendarId='primary', body=event).execute()

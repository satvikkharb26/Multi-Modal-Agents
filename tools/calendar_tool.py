import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import GOOGLE_CALENDAR_CREDENTIALS_PATH

def create_calendar_event(summary: str, start_time: str, duration_minutes=60):
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CALENDAR_CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    service = build("calendar", "v3", credentials=credentials)

    start_dt = datetime.datetime.fromisoformat(start_time)
    end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

    event = {
        "summary": summary,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "UTC"}
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event.get("htmlLink")

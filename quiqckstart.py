import datetime
import os.path
from time import strftime as t
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class GoogleCalendar():
  def get_events(self):
    creds = None
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file("dist/config.json", SCOPES)
        creds = flow.run_local_server(port=0)
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
      service = build("calendar", "v3", credentials=creds)
      now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
      events_result = (service.events().list(
              calendarId="primary",
              timeMin=now,
              singleEvents=True,
              orderBy="startTime",
          ).execute())
      return events_result.get("items", [])
    except HttpError as error: print(f"An error occurred: {error}")


if __name__ == "__main__":
  g = GoogleCalendar()
  eventos = g.get_events()
  for evento in eventos:
    print(evento['summary'])
    break

import datetime
import os.path
import pandas as pd
from dataframe_image import export
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendar():
  def get_events(self):
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds = None
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file("config.json", SCOPES)
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
              maxResults=30,
              orderBy="startTime",
          ).execute())
      return events_result.get("items", [])
    except HttpError as error: print(f"An error occurred: {error}")

  def criar_imagem(self):
    eventos = self.get_events()
    nome = []
    horario = []
    col = {'Data':''}
    for evento in eventos:
      nome.append(evento['summary'])
      for item in evento['start']:
        if item == 'dateTime': horario.append(evento['start']['dateTime'])
        elif item == 'date': horario.append(evento['start']['date'])

    df = pd.DataFrame(index=nome, data=horario, columns=col)
    export(df, 'dist/calendar.png')
    return 'dist/calendar.png'
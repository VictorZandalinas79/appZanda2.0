import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

def init_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        {
            "type": os.getenv("GOOGLE_TYPE"),
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
        },
        scope
    )
    return gspread.authorize(creds)

def export_to_sheets(events_df, players_list, rival_name):
    client = init_google_sheets()
    
    # Create new spreadsheet with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    spreadsheet_name = f"Partido_{timestamp}"
    sh = client.create(spreadsheet_name)
    
    # Export events
    events_worksheet = sh.add_worksheet(title="Eventos", rows=len(events_df)+1, cols=len(events_df.columns))
    events_worksheet.update([events_df.columns.values.tolist()] + events_df.values.tolist())
    
    # Export players
    players_df = pd.DataFrame(players_list, columns=["Jugador"])
    players_worksheet = sh.add_worksheet(title="Jugadores", rows=len(players_df)+1, cols=1)
    players_worksheet.update([["Jugador"]] + [[player] for player in players_list])
    
    return sh.url
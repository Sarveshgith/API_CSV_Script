import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "local-snow-444516-u5-b239abff2ec4.json"
sheet_id = '1AODVxKmEH5bKiB_Sx-9hvRyOxnOhklma1K01puz9RT'

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
try:
    sheet_write = sheet.values().update(
        spreadsheetId=sheet_id,
        range='A1',
        valueInputOption='RAW',
        body={'values': [['Hello', 'World']]}
    ).execute()
    print("Test successful!")
except Exception as e:
    print(f"Error: {e}")
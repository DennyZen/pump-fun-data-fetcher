from google.oauth2 import service_account
from googleapiclient.discovery import build
import os


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SERVICE_ACCOUNT_FILE = 'another.json'
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), SERVICE_ACCOUNT_FILE)

SAMPLE_SPREADSHEET_ID = '1UHL0RqUcDh7DqDz76IGPcLPgqSlkFzMenVZ3Y8LoRJk'
SAMPLE_RANGE_NAME = 'New Coins'

def write_to_google_sheets(data, cell='A1'):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    range_name = f"{SAMPLE_RANGE_NAME}!A:A"  # Assuming the column A is used for row numbers
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    last_row = len(values) + 1
    cell='A'+str(last_row)
    range_name = f"{SAMPLE_RANGE_NAME}!{cell}"
    print(range_name)
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range=range_name,
                                   valueInputOption="USER_ENTERED",
                                   body={"values":data}).execute()
    print(result)

to_write = [['testiiiiim','2222']]
write_to_google_sheets(to_write, cell='A6')
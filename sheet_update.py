from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1MLwVq41b1MHIONicCp3l6ip_AgSXJpjH6WxS0jY_sQA'
SAMPLE_RANGE_NAME = 'Sheet1!A1:C200'
EDIT_SAMPLE_RANGE = 'Sheet2!A1:A2000'
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = service_account.Credentials.from_service_account_file('token.json')
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

def read_data():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    return values

def write_data(data):
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=EDIT_SAMPLE_RANGE, valueInputOption="RAW", body={'values': [data]}).execute()



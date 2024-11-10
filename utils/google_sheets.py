
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import tempfile

def update_google_sheet(results_df: pd.DataFrame, credentials_file) -> str:
    """
    Update Google Sheet with extraction results.
    Returns the sheet URL.
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    try:
        # Save credentials file temporarily for Google API use
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(credentials_file.getvalue())
            temp_credentials_path = temp_file.name

        credentials = service_account.Credentials.from_service_account_file(
            temp_credentials_path, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        
        spreadsheet = {
            'properties': {'title': 'Extraction Results'}
        }
        
        spreadsheet = service.spreadsheets().create(
            body=spreadsheet,
            fields='spreadsheetId'
        ).execute()
        
        SPREADSHEET_ID = spreadsheet.get('spreadsheetId')
        
        values = [results_df.columns.tolist()] + results_df.values.tolist()
        
        body = {
            'values': values
        }
        
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        return f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
        
    except Exception as e:
        raise Exception(f"Google Sheets update failed: {str(e)}")

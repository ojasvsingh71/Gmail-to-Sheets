from googleapiclient.discovery import build
import config

# Tip: In a real scenario, we might separate auth logic entirely, 
# but for this assignment, reusing the token from the Gmail flow works since scopes are combined.

def get_sheets_service(creds=None):
    """Returns the Sheets service object."""
    # We can reuse the credentials if passed, or rebuild (omitted for brevity, usually shared)
    # For simplicity in this script, we can rely on the same auth flow used in main.
    # See main.py for how we pass credentials.
    pass 

def check_and_add_headers(service, spreadsheet_id):
    """
    Checks if the first row has the correct headers. 
    If not, it writes them.
    Required Columns: From, Subject, Date, Content.
    """
    range_name = 'Sheet1!A1:D1'
    
    # 1. Read the first row
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    required_headers = ['From', 'Subject', 'Date', 'Content']

    # 2. If row is empty or headers don't match, write them
    if not values or values[0] != required_headers:
        print("Headers missing or incorrect. Adding headers...")
        body = {
            'values': [required_headers]
        }
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
    else:
        print("Headers verified.")

def append_to_sheet(service, spreadsheet_id, data):
    """Appends a row of data [From, Subject, Date, Content] to the sheet."""
    body = {
        'values': [data]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A1', # Adjust Sheet name if needed
        valueInputOption='RAW',
        body=body
    ).execute()
    return result
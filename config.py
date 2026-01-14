import os

# Scopes: Read/Modify Gmail, Read/Write Sheets
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials', 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json') # Stores the user's access token

# Spreadsheet ID (Create a new Google Sheet and paste its ID here)
SPREADSHEET_ID = '181-To16V5p4Wwes9RSLd6nah9SkisW1vZDua3-nJ-lg'
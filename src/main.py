import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("project.log"), # Saves logs to a file
        logging.StreamHandler()             # Prints to console
    ]
)

# Add the project root to python path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sheets_service import append_to_sheet,check_and_add_headers
from src.gmail_service import get_gmail_service, fetch_unread_messages
from src.email_parser import parse_email_data
from googleapiclient.discovery import build
import config

def main():
    logging.info("Starting application...")
    # 1. Authenticate (Unified scope covers both Gmail and Sheets)
    gmail_service = get_gmail_service()

    logging.info("Authentication successful.")
    
    # Extract credentials from the gmail service object to build sheets service
    creds = gmail_service._http.credentials
    sheets_service = build('sheets', 'v4', credentials=creds)

    print("Checking for unread emails...")
    messages = fetch_unread_messages(gmail_service)

    if not messages:
        print("No new emails found.")
        return
    logging.info(f"Found {len(messages)} unread emails.")   

    logging.info("Checking Sheet configuration...")
    try:
        check_and_add_headers(sheets_service, config.SPREADSHEET_ID)
    except Exception as e:
        print(f"Error setting up headers: {e}")
        return

    for message in messages:
        msg_id = message['id']
        
        try:
            # 2. Parse Email
            email_data = parse_email_data(gmail_service, msg_id)
            logging.info(f"Successfully processed email: {email_data[1]}")

            # 3. Append to Sheets
            body = {'values': [email_data]}
            sheets_service.spreadsheets().values().append(
                spreadsheetId=config.SPREADSHEET_ID,
                range='Sheet1!A1',
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()

            # 4. State Management: Mark as Read
            # This ensures we don't process it again next time.
            gmail_service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
        except Exception as e:
            logging.error(f"Failed to process message {msg_id}: {e}")

    logging.info("All Done!")

if __name__ == '__main__':
    main()
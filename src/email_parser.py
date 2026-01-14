import base64
import re
from bs4 import BeautifulSoup

def clean_body(data):
    """Decodes email body and strips HTML to plain text."""
    if not data:
        return ""
    try:
        decoded_bytes = base64.urlsafe_b64decode(data)
        text = decoded_bytes.decode('utf-8')
        # Bonus: Strip HTML tags to satisfy "plain text" requirement
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text().strip()
    except Exception:
        return ""

def get_email_only(header_value):
    """Extracts just the email address from 'Name <email>' format."""
    # Regex to find email inside < > or just return the value if no brackets
    match = re.search(r'<([^>]+)>', header_value)
    if match:
        return match.group(1)
    return header_value.strip()

def parse_email_data(service, msg_id):
    """
    Fetches full email details and parses required fields.
    Returns: [Sender Email, Subject, Date, Content]
    """
    try:
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        payload = msg['payload']
        headers = payload.get('headers', [])

        sender = "Unknown"
        subject = "No Subject"
        date = "Unknown"

        # 1. Extract Headers
        for h in headers:
            if h['name'] == 'From':
                # Requirement: "Sender email address" (remove the name)
                sender = get_email_only(h['value']) 
            elif h['name'] == 'Subject':
                subject = h['value']
            elif h['name'] == 'Date':
                date = h['value']

        # 2. Extract Body (Content)
        content = ""
        if 'parts' in payload:
            for part in payload['parts']:
                # Prioritize plain text
                if part['mimeType'] == 'text/plain':
                    content = part['body'].get('data', '')
                    break
                # Fallback to HTML if no plain text
                elif part['mimeType'] == 'text/html' and not content:
                    content = part['body'].get('data', '')
        else:
            # Fallback if no multipart
            content = payload['body'].get('data', '')

        clean_content = clean_body(content)

        # STRICT ORDER: From, Subject, Date, Content
        return [sender, subject, date, clean_content]

    except Exception as e:
        print(f"Error parsing message {msg_id}: {e}")
        return None
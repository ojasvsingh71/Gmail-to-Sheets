# Gmail to Google Sheets Automation

## 1. Project Overview
This tool automates the extraction of incoming emails from a Gmail inbox and logs them into a Google Sheet. It uses OAuth 2.0 for secure authentication and handles duplicate prevention by tracking the "Unread" status of emails.

## Video Explaination & Screenshots :- [Link](https://drive.google.com/drive/folders/1Cl75ZbXR6OEqiBdryJHjo7Qpsw8FFrpY?usp=sharing)

## 2. Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Place `credentials.json` in the `credentials/` folder.
4. Update `config.py` with your `SPREADSHEET_ID`.
5. Run: `python src/main.py`

## 3. Design Decisions 
* **OAuth Flow:** Used the "Desktop App" flow to generate a user token (`token.json`). This ensures no sensitive passwords are stored in the code.
* **State Persistence:** The system relies on Gmail's `UNREAD` label. Emails are only fetched if they are unread. Once processed, the script removes the label, ensuring they are not fetched in the next run.
* **Duplicate Prevention:** By modifying the email state on the server (marking as read) immediately after processing, we prevent the same email from being added twice.

## 4. Challenges Faced 
* **Issue:** Initially faced `HttpError 404` when trying to append data.
* **Solution:** I realized the `SPREADSHEET_ID` in `config.py` was a placeholder. I debugged this by inspecting the API error logs and correcting the ID from the sheet's URL.

## 5. Limitations 
* The script currently only parses `text/plain` content perfectly; complex HTML emails might lose some formatting (though BeautifulSoup is used to clean it).
* It requires manual re-authentication if the `token.json` expires or is deleted.

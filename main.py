from creds.creds import API_KEY

import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def main():

    # If modifying these SCOPES, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('creds/token.json'):
        creds = Credentials.from_authorized_user_file('creds/token.json')

    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds/token.json', SCOPES)  # Path to your downloaded credentials.json
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('creds/token.json', 'w') as token:
            token.write(creds.to_json())

    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # Fetch last 10 emails
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        print(msg['snippet'])

if __name__ == '__main__':
    main()
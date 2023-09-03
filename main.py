from __future__ import print_function

import os.path
import pickle
from tqdm import tqdm

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils import increment_sender

def main():

    # Set up OAuth 2.0 credentials
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Initialize variables for pagination
    page_token = None
    messages = []
    sender_count = {}

        # Loop through pages of message metadata
    while True:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], pageToken=page_token).execute()
        messages.extend(results.get('messages', []))
        page_token = results.get('nextPageToken')
        if not page_token:
            break

    try:

        # Process each email
        for message in tqdm(messages):
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            sender = ''

            for header in msg['payload']['headers']:
                if header['name'] == 'From':
                    sender = header['value']

            sender = increment_sender(sender_count, sender)

    except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    # Sort senders by most occurring emails

    with open('sender_count.pkl', 'wb') as f:
        pickle.dump(f, sender_count)

if __name__ == '__main__':
    main()

from __future__ import print_function

import os.path
import pickle
from tqdm import tqdm

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils import increment_sender, sort_dict_by_values

def main():

    # Set up OAuth 2.0 credentials
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
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

    email_adresses = [
        'cineplex@ecampaigns.cineplex.com',
        'no-reply@forexprosmail.com',
        'no-reply@news.crypto.com',
        'hello@opensnow.com',
        'announcements@naylormarketing.com',
        'info@e.ipage.com',
        'NoReply@e.radissonhotelsamericas.com',
        'employees.ezpost@ualberta.ca',
        'reply@email.livenation.com'
    ]

    for email_address in email_adresses:

        # Specify the sender's email address
        sender_email = email_address

        # Initialize variables for pagination
        page_token = None

        # Loop through pages of message metadata
        while True:

            # Get a list of message IDs from the sender
            results = service.users().messages().list(userId='me', q=f"from:{sender_email}").execute()
            message_ids = [message['id'] for message in results.get('messages', [])]

            # Delete each email by moving it to the trash
            for message_id in message_ids:
                service.users().messages().trash(userId='me', id=message_id).execute()

            print(f"Deleted {len(message_ids)} emails from {sender_email}")
            page_token = results.get('nextPageToken')
            if not page_token:
                break

if __name__ == '__main__':
    main()

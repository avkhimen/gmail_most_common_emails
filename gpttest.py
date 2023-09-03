from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up OAuth 2.0 credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
credentials = flow.run_local_server(port=0)

# Build Gmail API service
service = build('gmail', 'v1', credentials=credentials)

# Initialize variables for pagination
page_token = None
messages = []

# Loop through pages of message metadata
while True:
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], pageToken=page_token).execute()
    messages.extend(results.get('messages', []))
    page_token = results.get('nextPageToken')
    if not page_token:
        break

# Process each email
for message in messages:
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    subject = ''
    sender = ''

    for header in msg['payload']['headers']:
        if header['name'] == 'Subject':
            subject = header['value']
        elif header['name'] == 'From':
            sender = header['value']

    print(f"Subject: {subject}")
    print(f"Sender: {sender}")
    print("-----")

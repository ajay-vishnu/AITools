import os

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up the credentials
SCOPES = {'read': 'https://www.googleapis.com/auth/gmail.readonly', 'compose': 'https://www.googleapis.com/auth/gmail.compose','modify': 'https://www.googleapis.com/auth/gmail.modify'}

def Service(type: str) -> build:
    creds = None

    if os.path.exists(f'JSON/{type}_token.json'):
        creds = Credentials.from_authorized_user_file(f'JSON/{type}_token.json', SCOPES[type])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'JSON/credentials.json', SCOPES[type])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f'JSON/{type}_token.json', 'w') as token:
            token.write(creds.to_json())

    # Return a Gmail API service instance
    return build('gmail', 'v1', credentials=creds)

if __name__ == '__main__':
    service = Service("modify")
import base64

import os

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText

# Set up the credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    message['from'] = sender
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def main():
    creds = None

    if os.path.exists('JSON/reply_token.json'):
        creds = Credentials.from_authorized_user_file('JSON/reply_token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'JSON/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('JSON/reply_token.json', 'w') as token:
            token.write(creds.to_json())

    # Create a Gmail API service instance
    service = build('gmail', 'v1', credentials=creds)

    # Find the message you want to reply to
    query = "subject:Test Email"
    result = service.users().messages().list(userId='me', q=query).execute()
    msg_id = result['messages'][0]['id']

    # Retrieve the message and its thread
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    # print(msg['payload']['headers'])
    thread_id = msg['threadId']

    # Create a reply message
    reply = "This is a sample reply message."
    body = reply
    message = create_message("me", "zain.khazi.777@gmail.com", "Reply to your email", body)
    message['threadId'] = thread_id

    # Send the reply message
    send_message = service.users().messages().send(userId='me', body=message).execute()
    print(F'sent message to {send_message["to"]}')

if __name__ == '__main__':
    main()
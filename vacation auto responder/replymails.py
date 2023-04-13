import base64

import os
from dotenv import load_dotenv

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText

load_dotenv()

# Set up the credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CONNECTED_MAIL = os.environ.get('MAIL')

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
    result = service.users().messages().list(userId='me', maxResults=10).execute()
    msg_ids = [i['id'] for i in result['messages']]

    # Retrieve the message and its thread
    msgs = [service.users().messages().get(userId='me', id=msg_id, format='full').execute() for msg_id in msg_ids]

    # Get the senders' mails
    threads = []
    for i in range(len(msgs)):
        headers = msgs[i]['payload']['headers']
        for header in headers:
            if header['name'] == 'From' and header['value'] != CONNECTED_MAIL:
                threads.append((msgs[i]['id'], msgs[i]['threadId'], header['value']))

    label_body = {
    'removeLabelIds': ['IMPORTANT', 'CATEGORY_UPDATES', 'INBOX', 'UNREAD'],
    'addLabelIds': ["Label_1"]
    }

    for msg_id, thread_id, to_mail in threads:
        # Create areply messages
        reply = "I'm immensely pleasured to tell you that the test that's conducted has been successful. Thank you for the support."
        body = reply
        message = create_message("me", to_mail, "Thank you for the test", body)
        message['threadId'] = thread_id

        # Send the reply message
        send_message = service.users().messages().send(userId='me', body=message).execute()

        # Add label to the message
        label_message = service.users().messages().modify(userId='me', id=msg_id, body=label_body).execute()
        print(send_message, label_message)

if __name__ == '__main__':
    main()
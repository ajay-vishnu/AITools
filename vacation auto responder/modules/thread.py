from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTED_MAIL = os.environ.get('MAIL')

def Threads(service: build) -> list:
    # Get the messages you want to reply to
    result = service.users().messages().list(userId='me', labelIds=["INBOX"], maxResults=10).execute()
    msg_ids = [i['id'] for i in result['messages']]

    # Retrieve the message and its thread
    msgs = [service.users().messages().get(userId='me', id=msg_id, format='full').execute() for msg_id in msg_ids]

    # Get the senders' mails
    threads = []
    for i in range(len(msgs)):
        headers = msgs[i]['payload']['headers']
        for header in headers:
            if header['name'] == 'From' and "Label_1" not in msgs[i]['labelIds'] and header['value'] != CONNECTED_MAIL:
                threads.append((msgs[i]['id'], msgs[i]['threadId'], header['value']))
    
    return threads

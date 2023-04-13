import base64

from email.mime.text import MIMEText

from modules.service import Service
from modules.thread import Threads

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    message['from'] = sender
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def main():

    # Create a Gmail API service instance
    service = Service(type="modify")

    # Get the senders' mails
    threads = Threads(service)

    label_body = {
    'removeLabelIds': ['IMPORTANT', 'CATEGORY_UPDATES', 'INBOX', 'UNREAD'],
    'addLabelIds': ["Label_1"]
    }

    for msg_id, thread_id, to_mail in threads:
        # Create a reply message
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
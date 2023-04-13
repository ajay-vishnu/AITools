import base64

from email.mime.text import MIMEText

from modules.thread import Threads

LABEL_BODY = {
'removeLabelIds': ['IMPORTANT', 'CATEGORY_UPDATES', 'INBOX', 'UNREAD'],
'addLabelIds': ["Label_1"]
}

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    message['from'] = sender
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def Replymails(service):
    # Get the senders' mails
    threads = Threads(service)

    for msg_id, thread_id, to_mail in threads:
        response = []
        # Create a reply message
        reply = "I'm immensely pleasured to tell you that the test that's conducted has been successful. Thank you for the support."
        body = reply
        message = create_message("me", to_mail, "Thank you for the test", body)
        message['threadId'] = thread_id

        # Send the reply message
        send_message = service.users().messages().send(userId='me', body=message).execute()

        # Add label to the message
        label_message = service.users().messages().modify(userId='me', id=msg_id, body=LABEL_BODY).execute()
        response.append((send_message, label_message))
    
    return response
import os.path
from time import sleep

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timezone
import email


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']


def remove_token():
    try:
        file_path = 'token.json'
        os.remove(file_path)
        print(f"File '{file_path}' has been removed successfully")
    except OSError as error:
        print(f"Error: {error} - '{file_path}' file cannot be removed")


def create_gmail_credential():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(
            'token.json', SCOPES)

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
    return creds


def build_gmail_service(creds):
    service = build('gmail', 'v1', credentials=creds)
    return service


def check_authentication_success(service):
    try:
        profile = service.users().getProfile(userId='me').execute()
        return True, profile
    except HttpError as error:
        print('An error occurred: %s' % error)
        return False, None


def logout(service):
    try:
        service.users().stop(userId='me').execute()
        remove_token()
    except HttpError as error:
        print(f"An error occurred: {error}")
    # handle the error


def create_gmail_message(to, subject, message_text):
    message = MIMEMultipart()
    text = MIMEText(message_text)
    message.attach(text)
    message['to'] = to
    message['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(
        message.as_bytes()).decode()}
    return create_message


def gmail_send_message(service, message):
    try:
        message = (service.users().messages().send(
            userId="me", body=message).execute())

        thread_id = message['threadId']
        print(F'Thread Id: {message["threadId"]}')
    except Exception as error:
        print(F'An error occurred: {error}')
        message = None
        thread_id = None

    return message, thread_id


# function to fetch and print replies to an email thread
def fetch_gmail_replies(service, thread_id):
    try:
        response = service.users().threads().get(
            userId='me', id=thread_id).execute()
        messages = response['messages']
        print('Number of messages in thread: %d' % len(messages))
        print("messages:", messages)
        for message in messages:
            # only consider messages in Inbox
            if 'INBOX' in message['labelIds']:
                print("---------------------------\nINBOX")
                headers = message['payload']['headers']

                sender = 'anonymous'
                for header in headers:
                    if header['name'] == 'From':
                        sender = header['value']

                    if header['name'] == "Date":
                        date = header['value']
                        date = date.split("+")[0].strip()

                body = message['snippet']
                body = body.split("&amp;&amp;&amp;")[0].strip()

                print('Reply from: %s\nDatetime: %s\nBody: %s\n' %
                      (sender, date, body))
                return sender, date, body
        return None, None, None

    except HttpError as error:
        print('An error occurred: %s' % error)
        return None, None, None


def BindIncomingEmails(service, thread_id):
    while True:
        try:
            sender, date, body = fetch_gmail_replies(service, thread_id)

            if (sender is not None) and (date is not None) and (body is not None):
                return sender, date, body

            sleep(5)
        except:
            pass


def main():
    try:
        # create credential
        creds = create_gmail_credential()

        # build service
        service = build_gmail_service(creds)

        check_authentication_success(service)

        # send email
        to = 'quannguyenthanh558@gmail.com'
        subject = 'Test Email'
        message_text = 'This is a test email sent through Gmail API.'

        message = create_gmail_message(to, subject, message_text)
        message, thread_id = gmail_send_message(service, message)

        while True:
            sender, date, body = fetch_gmail_replies(service, thread_id)

            if (sender is not None) and (date is not None) and (body is not None):
                break

            print("---")
            sleep(5)

        # logout(service)

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()

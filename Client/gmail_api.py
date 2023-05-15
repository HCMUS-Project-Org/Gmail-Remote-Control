import os
import os.path
from pathlib import Path
from time import sleep
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


def setup_path(file_path):
    # Set up the path to the file.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, file_path)

    return path


dotenv_path = Path('../.env')
load_dotenv()  # take environment variables from .env.


SERVER_EMAIL = os.getenv("SERVER_EMAIL")
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.modify']
ASSET_PATH = setup_path("./static/assets/received_files")


def create_asset_folder():
    if not os.path.exists(ASSET_PATH):
        os.makedirs(ASSET_PATH)


def remove_token():
    try:
        file_path = setup_path('token.json')
        os.remove(file_path)
        print(f"[Info] File '{file_path}' has been removed successfully")
    except OSError as error:
        print(
            f"[Remove token] Error: {error} - '{file_path}' file cannot be removed")


def create_gmail_credential():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(setup_path('token.json')):
        creds = Credentials.from_authorized_user_file(
            setup_path('token.json'), SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    setup_path('credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            except:
                creds = None
                return creds
        # Save the credentials for the next run
        with open(setup_path('token.json'), 'w') as token:
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
        print('[Check authentication success] An error occurred: %s' % error)
        return False, None


def logout(service):
    try:
        print("[Info] Logging out...")
        service.users().stop(userId='me').execute()
        remove_token()
        print("[Info] Logged out successfully")
    except HttpError as error:
        print(f"[Logout] An error occurred: {error}")
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
        print(F'[Info] Sent message (msg thread Id: {message["threadId"]})')
    except Exception as error:
        print(F'[Gmail send msg] An error occurred: {error}')
        message = None
        thread_id = None

    return message, thread_id


def download_attachment(service, message_id):
    """Get and store attachment from Message with given id.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_id: ID of Message containing attachment.
    prefix: prefix which is added to the attachment filename on saving
    """
    try:
        print("[Info] Start downloading attachment...")

        message = service.users().messages().get(userId='me', id=message_id).execute()

        for part in message['payload']['parts']:
            if part['mimeType'] == "multipart/mixed":
                for prt in part['parts']:
                    newvar = prt['body']
                    if 'attachmentId' in newvar:
                        att_id = newvar['attachmentId']
                        att = service.users().messages().attachments().get(
                            userId='me', messageId=message_id, id=att_id).execute()
                        data = att['data']

                        file_data = base64.urlsafe_b64decode(
                            data.encode('UTF-8'))
                        print("- Download: ", prt['filename'])

                        # save file
                        path = os.path.join(ASSET_PATH, prt['filename'])

                        with open(path, 'wb') as f:
                            f.write(file_data)
                            f.close()
        print("[Info] Downloading attachment completed")
    except HttpError as error:
        print('[Download attachment] An error occurred: %s' % error)


def read_email(service):
    # Call the Gmail API to fetch the latest emails from the inbox
    print("[Info] Fetch a list of the message")
    try:
        # Fetch a list of all the message IDs in the INBOX folder
        message_response = service.users().messages().list(userId='me').execute()

        # Get the 5 newly messages
        message_list = message_response['messages']
        message_list = message_list[:5]

        # Loop through each message in the list and print the subject and sender
        for message in message_list:
            message_id = message['id']
            message = service.users().messages().get(userId='me', id=message_id).execute()

            # only consider messages in Inbox
            if 'INBOX' in message['labelIds'] and 'UNREAD' in message['labelIds'] and 'IMPORTANT' in message['labelIds']:
                headers = message['payload']['headers']

                sender = 'anonymous'
                for header in headers:
                    if header['name'] == 'From':
                        sender = header['value']

                        if sender != SERVER_EMAIL:
                            return None, None, None

                    if header['name'] == "Date":
                        date = header['value']
                        date = date.split("+")[0].strip()

                # download attachment
                download_attachment(service, message_id)

                # get body
                body_content = ''
                body_parts = message['payload']['parts'][0]['parts']
                for part in body_parts:
                    if part['mimeType'] == "text/html":
                        body = part['body']['data']
                        body_content += base64.urlsafe_b64decode(
                            body.encode('UTF-8')).decode('UTF-8')

                print('[Info] Server reply:')
                print('- Reply from: %s\n- Datetime: %s\n- Body: %s\n' %
                      (sender, date, body_content))

                # Add label to the email to mark it as read
                service.users().messages().modify(
                    userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()

                # return result
                return sender, date, body_content
        return None, None, None

    except HttpError as error:
        print(f'[Read email] An error occurred: {error}')
        return None, None, None


def bind_incoming_emails(service):
    print("[Info] Bind incoming emails")
    while True:
        try:
            # sender, date, body = fetch_gmail_replies(service, thread_id)
            sender, date, body = read_email(service)

            if (sender is not None) and (date is not None) and (body is not None):
                print("[Info] Bind incoming emails completed")
                return sender, date, body

            sleep(10)
        except:
            pass


def main():
    try:
        create_asset_folder()

        # create credential
        creds = create_gmail_credential()

        # build service
        service = build_gmail_service(creds)

        # check_authentication_success(service)

        # # send email
        # to = 'quannguyenthanh558@gmail.com'
        # subject = 'Test Email'
        # message_text = 'This is a test email sent through Gmail API.'

        # message = create_gmail_message(to, subject, message_text)
        # message, thread_id = gmail_send_message(service, message)

        while True:
            sender, date, body = read_email(service)
            # sender, date, body = fetch_gmail_replies(
            #     service, "1881362dc08f0e03")

            if (sender is not None) and (date is not None) and (body is not None):
                break

            print("---")
            sleep(10)

        # logout(service)
        # download_attachment(service, "187a1a3561d66ff3")

    except HttpError as error:
        print(f'[Main] An error occurred: {error}')


if __name__ == '__main__':
    main()

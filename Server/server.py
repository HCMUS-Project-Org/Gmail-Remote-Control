# Work with Image
import service.capture_screen as cs
import service.capture_webcam as cw
import service.mac_address as mac
import service.app_process as ap
import os
import imaplib
import smtplib
import time
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from service.shared_function import *
import datetime


# Global variables
global client
BUFSIZ = 1024 * 4

user = "quannguyenthanh16@gmail.com"
password = 'bjxuzmxcmpqserll'

imap_url = 'imap.gmail.com'
smtp_url = 'smtp.gmail.com'


command = []


def create_asset_folder():
    if not os.path.exists(ASSET_PATH):
        os.makedirs(ASSET_PATH)


def connect():
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL(imap_url, 993)
    smtp = smtplib.SMTP_SSL(smtp_url)

    # authenticate imap and smtp
    try:
        imap.login(user, password)
        smtp.login(user, password)
        # rest of your code for reading emails
    except imaplib.IMAP4.error as e:
        print(f"Login failed. Reason: {e}")

    return imap, smtp


def send_mail(smtp, user, sender, subject):
    # Send a reply message to the sender
    reply_msg = MIMEMultipart()
    # reply_msg['From'] = f'Mail server TelePC <{user}>'
    reply_msg['From'] = user
    reply_msg['To'] = sender
    reply_msg['Subject'] = subject
    reply_content = """
        <p><b>Bold text</b></p>
        <p><u>Underlined text</u></p>
        <p><i>Italicized text</i></p>
    """
    reply_msg.attach(MIMEText(reply_content, 'html'))
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
                # function(content)

                # reply back to sender
                send_mail(smtp, user, sender, subject='test',)

        # Sleep for 10 second before checking for new emails again
        time.sleep(10)


def function(msg):
    if "SCREEN" in msg:
        cs.capture_screen()
    elif "WEBCAM" in msg:
        cw.capture_webcam_image()
    elif "MAC" in msg:
        mac.mac_address()
    elif "APP_PRO" in msg:
        ap.app_process()

    # # capture the screen
    # server.capture_screen()

    # # get the mac address
    # mac_address = server.get_mac_address()
    # print(mac_address)

    # capture an image by the camera
    # server.capture_webcam_image()


if __name__ == "__main__":
    create_asset_folder()

    msg = "SCREEN"

    imap, smtp = connect()
    receive_mail(imap, smtp)

    # logout and close mailbox #useless
    imap.logout()
    smtp.quit()

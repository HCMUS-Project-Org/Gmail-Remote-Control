import os
from gmail_api import *

from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
import glob


load_dotenv()  # take environment variables from .env.

SECRET_KEY = os.getenv("SECRET_KEY")
PORT = os.getenv("PORT")
SERVER_EMAIL = os.getenv("SERVER_EMAIL")
ASSET_PATH = "./static/assets/received_files"


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

Bootstrap(app)

# init gmail api
gmail_credential = None
gmail_service = None
thread_id = None
client_profile = {
    'emailAddress': None,
}


def create_asset_folder():
    if not os.path.exists(ASSET_PATH):
        os.makedirs(ASSET_PATH)


def remove_asset_file():
    files_path = os.path.join(ASSET_PATH, '/*')
    files = glob.glob(files_path)

    for f in files:
        os.remove(f)


def authorize():
    return os.path.exists(setup_path('token.json'))


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""

    if request.method == "POST":
        global client_profile, gmail_credential, gmail_service

        # try:
        gmail_credential = create_gmail_credential()
        gmail_service = build_gmail_service(gmail_credential)
        # except:
        #     error = "You must grant permission to access your Gmail account"

        try:
            isSuccess, client_profile = check_authentication_success(
                gmail_service)
        except:
            isSuccess = False
            client_profile = {
                'emailAddress': None,
            }

        if isSuccess and error == "":
            print("AUTHENTICATION: Success")
            print("CLIENT PROFILE:", client_profile)

            return redirect(url_for('control'))
        else:
            print("AUTHENTICATION: Fail")
            if error == "":
                error = "Authentication failed"

    return render_template('login.html', error=error)


@app.route('/disconnect', methods=['GET', 'POST'])
def disconnect():
    try:
        logout(gmail_service)
    except:
        pass

    return redirect(url_for('login'))


@app.route('/control', methods=['GET', 'POST'])
def control():
    try:
        remove_asset_file()
    except:
        pass

    # authorize user
    if not authorize():
        return render_template('control.html', client_email=client_profile['emailAddress'], server_email=SERVER_EMAIL, isAuthor=False)

    return render_template('control.html', client_email=client_profile['emailAddress'], server_email=SERVER_EMAIL,  isAuthor=True)


@app.route('/review', methods=['GET', 'POST'])
def review():
    if not authorize():
        return redirect(url_for('login'))

    sender, date, body = None, None, None
    if request.method == "GET":
        # sender, date, body = bind_incoming_emails(
        #     gmail_service, thread_id)
        sender, date, body = 'quan', '2021-05-20', "Hello"

    return render_template('review.html', client_email=client_profile["emailAddress"], server_email=SERVER_EMAIL, date=date, body=body)


@app.route('/send-request', methods=['GET', 'POST'])
def send_request():
    # authorize user
    if not authorize():
        return redirect(url_for('login'))

    if request.method == "POST":
        global thread_id

        data = request.get_json()

        print("data:", data)

        # email content
        to = SERVER_EMAIL
        subject = 'Control Request'
        message_text = data["content"].replace("<br/>", "\n")

        print("message_txt:", message_text)
        # create and send email
        message = create_gmail_message(to, subject, message_text)
        print("message:", message)

        message, thread_id = gmail_send_message(gmail_service, message)
        print("thread_id:", thread_id)

    return redirect(url_for('review'))


@app.route('/another-request', methods=['GET', 'POST'])
def new_request():
    # authorize user
    if not authorize():
        return redirect(url_for('login'))

    return redirect(url_for('control'))


if __name__ == '__main__':
    create_asset_folder()
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)

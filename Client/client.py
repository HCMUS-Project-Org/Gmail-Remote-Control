import os
from gmail_api import *

from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
import glob

dotenv_path = Path('../.env')
load_dotenv()  # take environment variables from .env.

SECRET_KEY = os.getenv("SECRET_KEY")
PORT = os.getenv("PORT")
SERVER_EMAIL = os.getenv("SERVER_EMAIL")
ASSET_PATH = setup_path("./static/assets/received_files")


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
sender, date, body = None, None, None


def create_asset_folder():
    if not os.path.exists(ASSET_PATH):
        os.makedirs(ASSET_PATH)


def remove_asset_file():
    try:
        print("[Info] Remove all files in [received_files]")
        files_path = os.path.join(ASSET_PATH, '/*')
        files = glob.glob(files_path)

        for f in files:
            os.remove(f)
    except OSError as error:
        print(
            f"[Remove asset file] Error: {error} - '{files_path}' file cannot be removed")


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

        try:
            gmail_credential = create_gmail_credential()
            gmail_service = build_gmail_service(gmail_credential)
        except:
            error = "You must grant permission to access your Gmail account"

        try:
            isSuccess, client_profile = check_authentication_success(
                gmail_service)
        except:
            isSuccess = False
            client_profile = {
                'emailAddress': None,
            }

        if isSuccess and error == "":
            print("[Info] Authenticate: Success")
            print("[Info] client profile: ", client_profile)

            return redirect(url_for('control'))
        else:
            print("[Info] Authenticate: Fail")
            if error == "":
                error = "[Error] Authenticate failed"

    return render_template('login.html', error=error)


@app.route('/disconnect', methods=['GET', 'POST'])
def disconnect():
    logout(gmail_service)

    return redirect(url_for('login'))


@app.route('/anonymous-control', methods=['GET', 'POST'])
def anonymous_control():
    remove_token()
    return redirect(url_for('control'))


@app.route('/control', methods=['GET', 'POST'])
def control():
    remove_asset_file()

    # authorize user
    if not authorize():
        return render_template('control.html', client_email=client_profile['emailAddress'], server_email=SERVER_EMAIL, isAuthor=False)

    return render_template('control.html', client_email=client_profile['emailAddress'], server_email=SERVER_EMAIL,  isAuthor=True)


@app.route('/review', methods=['GET', 'POST'])
def review():
    global sender, date, body

    if not authorize():
        return redirect(url_for('login'))

    return render_template('review.html', client_email=client_profile["emailAddress"], server_email=SERVER_EMAIL, date=date, body=body)


@app.route('/send-request', methods=['GET', 'POST'])
def send_request():
    # authorize user
    if not authorize():
        return redirect(url_for('login'))

    if request.method == "POST":
        global thread_id

        data = request.get_json()

        # email content
        to = SERVER_EMAIL
        subject = 'TelePCEST'
        message_text = data["content"].replace("<br/>", "\n")

        # create and send email
        message = create_gmail_message(to, subject, message_text)
        message, thread_id = gmail_send_message(gmail_service, message)

        # get reply email
        global sender, date, body
        sender, date, body = bind_incoming_emails(gmail_service)
        body = body.replace("<br/>", "\n")

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

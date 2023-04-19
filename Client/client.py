import os
from gmail_api import *

try:
    from flask import Flask, render_template, redirect, url_for, request, Markup
    from dotenv import load_dotenv
    from flask_bootstrap import Bootstrap
except Exception:
    # import all package
    os.system("pip install -r requirements.txt")

    from flask import Flask, render_template, redirect, url_for, request, Markup
    from dotenv import load_dotenv
    from flask_bootstrap import Bootstrap


load_dotenv()  # take environment variables from .env.

SECRET_KEY = os.getenv("SECRET_KEY")
PORT = os.getenv("PORT")
SERVER_EMAIL = os.getenv("SERVER_EMAIL")

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

Bootstrap(app)

# init gmail api
gmail_credential = None
gmail_service = None
client_profile = {}

# TODO: auto insatll Library


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""

    if request.method == "POST":
        global client_profile, gmail_credential, gmail_service

        gmail_credential = create_gmail_credential()
        gmail_service = build_gmail_service(gmail_credential)

        isSuccess, client_profile = check_authentication_success(gmail_service)

        if isSuccess:
            print("AUTHENTICATION: Success")
            print("CLIENT PROFILE:", client_profile)
            return redirect(url_for('control'))
        else:
            print("AUTHENTICATION: Fail")
            error = "Authentication failed"

    return render_template('login.html', error=error)


@app.route('/disconnect', methods=['GET', 'POST'])
def disconnect():
    logout(gmail_service)
    return redirect(url_for('login'))


@app.route('/control', methods=['GET', 'POST'])
def control():
    print("server email:", SERVER_EMAIL)
    return render_template('control.html', client_email=client_profile['emailAddress'], server_email=SERVER_EMAIL)


@app.route('/review', methods=['GET', 'POST'])
def review():
    # if request.method == "POST":
    #     pass

    return render_template('review.html', client_email=client_profile["emailAddress"], server_email=SERVER_EMAIL)


@app.route('/send-request', methods=['GET', 'POST'])
def send_request():
    if request.method == "POST":
        global thread_id

        data = request.get_json()

        # email content
        to = SERVER_EMAIL
        subject = 'Control Request'
        message_text = data["content"].replace("<br/>", "\n")

        # create and send email
        message = create_gmail_message(to, subject, message_text)
        message, thread_id = gmail_send_message(gmail_service, message)

    return redirect(url_for('review'))


@app.route('/another-request', methods=['GET', 'POST'])
def new_request():
    return redirect(url_for('control'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)

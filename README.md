# Building a remote control program using E-Mail

<div align="center">
  <h4>
      <a href="https://www.youtube.com/channel/UCALhAytLBhmG2un43YxU4mw">View Demo</a>
    <span> · </span>
      <a href="https://docs.google.com/document/d/e/2PACX-1vSQ8F-4o7uORHc82Yc5bNDYR-bsX5j2SZyzEkiv02kIN-EfeR9NY5c9qcMFp8h_4-MBwU_9DVT9heWB/pub">Documentation</a>
  </h4>
</div>

## Table of contents

-  [Building a remote control program using E-Mail](#building-a-remote-control-program-using-e-mail)
   -  [Table of contents](#table-of-contents)
   -  [About the project](#about-the-project)
      -  [Introduction:](#introduction)
      -  [Technology:](#technology)
      -  [Features](#features)
   -  [Getting start](#getting-start)
      -  [Prerequisites](#prerequisites)
      -  [Run locally](#run-locally)
   -  [Description](#description)
      -  [Login](#login)
      -  [Control](#control)
      -  [Review](#review)
      -  [Ribbon bar](#ribbon-bar)
   -  [Member](#member)
   -  [References](#references)

## About the project

### Introduction:

Program to control remote computer by email, in which:

-  **The user** (client) sends an email (containing requests to be made by the server) to the server's email (server).
-  **The server** reads the incoming email, performs the tasks the client sends and sends the results back to the client by replying to the client's email.

### Technology:

-  **Framework:** Flask
-  **Backend:** Python
-  **Frontend:** HTML, CSS, JavaScript, Bootstrap 5

### Features

**Client application:** A web GUI app to control remote computer, in which:

-  Login with google account.
-  Send email to server.
-  Get and show reply email from server.
-  View detail and download attached files.

**Server application:**

-  Key logger: Get keystrokes from keyboard.
-  Shutdown/logout:
   -  Shutdown computer.
   -  Logout computer.
-  MAC address: Get computer's MAC address.
-  Save screenshot.
-  Capture webcam image.
-  Directory tree:
   -  List all files in a directory.
   -  Copy files to client computer.
   -  Copy files to server computer.
   -  Delete files.
-  App process:
   -  List processes.
   -  List applications.
   -  Kill processes.
   -  Start applications.
-  Registry:
   -  Get registry value.
   -  Set registry value.
   -  Create registry key.
   -  Delete registry key.

## Getting start

### Prerequisites

-  Python `>= 3.10.7`
-  Client environment variables:

   -  **Environment:** add file `.env` in `/Client`, `.env` config:

      -  `SECRET_KEY`: a key used by Flask to encrypt and sign session data.
      -  `PORT`: specify which port the Flask application should listen on.
      -  `SERVER_EMAIL`: the email address of the server, which is received email from client

      Example:

      ```bash
      # .env
      SECRET_KEY = "RemoteControlByEmail-HCMUS"
      PORT = 3000
      SERVER_EMAIL = "server@example.com"
      ```

   -  **Credentials:** get Gmail API credentials file by [Gmail API instruction](https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application) then add file `credentials.json` in `/Client`

      Example:

      ```json
      // credentials.json
      {
      	"installed": {
      		"client_id": "client_id.apps.googleusercontent.com",
      		"project_id": "gmail-remote-control",
      		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
      		"token_uri": "https://oauth2.googleapis.com/token",
      		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      		"client_secret": "client_secret",
      		"redirect_uris": ["http://localhost"]
      	}
      }
      ```

### Run locally

Clone the project:

```bash
git clone https://github.com/HCMUS-Project/Gmail-Remote-Control.git
```

Go to the project directory:

```bash
cd Gmail-Remote-Control
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
python Server/server.py
```

The server will run on port 5656 and with host 0.0.0.0

Start the client:

```bash
python Client/client
```

The client will run on PORT which define in `.env` file and with host:

-  Running on http://127.0.0.1:[PORT]
-  Running on http://192.168.133.135:[PORT]

## Description

### Login

<figure>
  <img src="./assets/login.png" alt="Login page"/>
  <figcaption>Login page</figcaption>
</figure>
User have 2 choice to using the program:

-  **Without google account**, in this option, user can use program in anonymous mode (In this feature, the user has to send and view the response manually, the program only helps the user to write valid commands to the server)
-  **Within google account**, in this option, user must provide read and send email permission (In this feature, the program will help you to send and view reply email)

### Control

<figure>
  <img src="./assets/control.png" alt="Control page"/>
  <figcaption>Control page</figcaption>
</figure>
Allow user selects the command to be executed by the server, the program will auto generate email and send to server.

### Review

<figure>
  <img src="./assets/review.png" alt="Review page"/>
  <figcaption>Review page</figcaption>
</figure>
The application will wait for the server to reply then display the result in the window. User can:
See the content of the reply mail
See the details of the attached file
Download the attached file to the Download folder

### Ribbon bar

<figure>
  <img src="./assets/ribbon-bar.png" alt="Ribbon bar"/>
  <figcaption>Ribbon bar</figcaption>
</figure>
The application will wait for the server to reply then display the result in the window. User can:

-  See the content of the reply mail
-  See the details of the attached file
-  Download the attached file to the
-  Download folder

## Member

-  19127392 - [To Gia Hao](https://github.com/To-Gia-Hao)
-  **19127525 - [Nguyen Thanh Quan](https://github.com/QuanBlue)**
-  19127625 - [Lam Chi Van](https://github.com/chivanz128)

## References

[Python 3.11 Document](https://docs.python.org/3/)
[Flask document](https://flask.palletsprojects.com/en/2.2.x/)  
[Youtube - MacOS big sur theme](https://www.youtube.com/watch?v=NVT5oQ_6_hU&ab_channel=MartinBozhurski)  
[Gmail API Document](https://developers.google.com/gmail/api/guides)  
[PIL Documentation](https://pillow.readthedocs.io/en/stable/)  
[Pynput Documentation](https://pynput.readthedocs.io/en/latest/)  
[Psutil Documentation](https://psutil.readthedocs.io/en/latest/)

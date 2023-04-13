import sys
import os
import tkinter as tk
import socket
# import keylogger_server as kl
import app_process_server as ap
import directory_tree_server as dt
import live_screen_server as lss
import mac_address_server as mac
import shutdown_logout_server as sl
import registry_server as rs

main = tk.Tk()
main.geometry("200x200")
main.title("Server")
main['bg'] = '#011111'

# Global variables
global client
BUFSIZ = 1024 * 4


def abs_path(file_name):
    file_name = 'assets\\' + file_name
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, file_name)

# def keylogger():
#     global client
#     kl.keylog(client)
#     return


def shutdown_logout():
    global client
    sl.shutdown_logout(client)
    return


def mac_address():
    global client
    mac.mac_address(client)
    return


def app_process():
    global client
    ap.app_process(client)
    return


def live_screen():
    global client
    lss.capture_screen(client)
    return
    return


def directory_tree():
    global client
    dt.directory(client)
    return


def registry():
    global client
    rs.registry(client)
    return

# Connect
###############################################################################


def Connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''
    port = 5656
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(100)
    global client
    client, addr = s.accept()
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        # if "KEYLOG" in msg:
        #     keylogger()
        if "SD_LO" in msg:
            shutdown_logout()
        elif "LIVESCREEN" in msg:
            live_screen()
        elif "APP_PRO" in msg:
            app_process()
        elif "MAC" in msg:
            mac_address()
        elif "DIRECTORY" in msg:
            directory_tree()
        elif "REGISTRY" in msg:
            registry()
        elif "QUIT" in msg:
            client.close()
            s.close()
            return
###############################################################################


button_image_open = tk.PhotoImage(file=abs_path("image_open.png"))
tk.Button(main,
          #   image=button_image_open,
          text="OPEN", width=10, height=2, fg='#011111', bg='#E9B04B', borderwidth=0,
          highlightthickness=0, command=Connect, relief="flat").place(x=100, y=100, anchor="center")
main.mainloop()

import os
from time import sleep
from . import shared_function as sf
import threading
#import shared_function as sf


def shutdown():
    if sf.check_os() == 'window':
        os.system("shutdown -s -t 0")
    else:
        os.system("shutdown -h now")


def logout():
    if sf.check_os() == 'window':
        os.system(f"shutdown -l")
    else:
        os.system(f"logout")


def shutdown_logout(function):
    result = None
    if "Shutdown" in function:
        result = "Server will shutdown in 30s"
        threading.Timer(30, shutdown).start()
    elif "Logout" in function:
        result = "Server will logout in 30s"
        threading.Timer(30, logout).start()
    return "</br><b>Shutdown/Logout:</b> " + result

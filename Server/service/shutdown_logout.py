import os
from time import sleep
from . import shared_function as sf


def shutdown(delay):
    '''Delay then shutdown the computer'''
    sleep(int(delay))

    if sf.check_os() == 'window':
        os.system("shutdown -s -t 0")
    else:
        os.system("shutdown -h now")


def logout():
    '''Log out the computer'''

    if sf.check_os() == 'window':
        os.system(f"shutdown -l")
    else:
        os.system(f"logout")

def shutdown_logout(function):
    if "Shutdown" in function:
        shutdown(5)
    else:
        logout()


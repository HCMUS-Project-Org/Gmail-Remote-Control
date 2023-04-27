import os
from time import sleep
from . import shared_function as sf
#import shared_function as sf

def shutdown(delay):
    '''Delay then shutdown the computer'''
    sleep(int(delay))

    if sf.check_os() == 'window':
        os.system("shutdown -s -t 0")
    else:
        os.system("shutdown -h now")


def logout(delay):
    '''Delay then Log out the computer'''
    sleep(int(delay))

    if sf.check_os() == 'window':
        os.system(f"shutdown -l")
    else:
        os.system(f"logout")

def shutdown_logout(function):
    #TODO: shutdown before it can send mail
    if "Shutdown" in function:
        shutdown(5)
        return "\nWindow shutdown"
    elif "Logout":
        logout(5)
        return "\nWindow shutdown"

shutdown_logout("Logout")
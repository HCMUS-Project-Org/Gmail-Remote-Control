import os
from time import sleep
from shared_function import *


def shutdown(delay):
    '''Delay then shutdown the computer'''
    sleep(int(delay))

    if check_os() == 'window':
        os.system("shutdown -s -t 0")
    else:
        os.system("shutdown -h now")


def logout():
    '''Log out the computer'''

    if check_os() == 'window':
        os.system(f"shutdown -l")
    else:
        os.system(f"logout")


if __name__ == "__main__":
    # shutdown(20)
    logout()

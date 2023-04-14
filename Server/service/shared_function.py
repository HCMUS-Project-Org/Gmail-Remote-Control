import os


def check_os():
    my_os = None

    if os.name == 'posix':
        my_os = "linux"
    elif os.name == 'nt':
        my_os = "window"

    return my_os

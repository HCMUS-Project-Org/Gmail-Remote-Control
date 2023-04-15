import os
from pathlib import Path


def check_os():
    my_os = None

    if os.name == 'posix':
        my_os = "linux"
    elif os.name == 'nt':
        my_os = "window"

    return my_os


def check_file_exist(file_path):
    '''check if file exist'''
    return os.path.exists(file_path)


def convert_to_path(file_path):
    '''convert file path to path object'''
    return Path(os.path.expanduser(file_path))

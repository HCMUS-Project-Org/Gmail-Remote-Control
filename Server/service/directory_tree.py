from itertools import islice
from pathlib import Path
import os
import shutil
from shared_function import *


def convert_to_path(file_path):
    '''convert file path to path object'''
    return Path(os.path.expanduser(file_path))


def check_file_exist(file_path):
    '''check if file exist'''
    return os.path.exists(file_path)


def show_directory_tree(root, deep_level=2):
    # prefix components:
    space = '    '
    branch = '│   '
    # pointers:
    tee = '├── '
    last = '└── '

    def tree(dir_path: Path, level: int = -1, limit_to_directories: bool = False,
             length_limit: int = 1000):
        """Given a directory Path object print a visual tree structure"""
        dir_path = Path(dir_path)  # accept string coerceable to Path
        files = 0
        directories = 0

        def inner(dir_path: Path, prefix: str = '', level=-1):
            nonlocal files, directories
            if not level:
                return  # 0, stop iterating
            if limit_to_directories:
                contents = [d for d in dir_path.iterdir() if d.is_dir()]
            else:
                contents = list(dir_path.iterdir())
            pointers = [tee] * (len(contents) - 1) + [last]
            for pointer, path in zip(pointers, contents):
                if path.is_dir():
                    yield prefix + pointer + path.name
                    directories += 1
                    extension = branch if pointer == tee else space
                    yield from inner(path, prefix=prefix+extension, level=level-1)
                elif not limit_to_directories:
                    yield prefix + pointer + path.name
                    files += 1
        print(dir_path.name)
        iterator = inner(dir_path, level=level)
        for line in islice(iterator, length_limit):
            print(line)
        if next(iterator, None):
            print(f'... length_limit, {length_limit}, reached, counted:')
        print(f'\n{directories} directories' +
              (f', {files} files' if files else ''))

    directory = convert_to_path(root)

    try:
        for line in tree(directory, level=deep_level, limit_to_directories=True):
            print(line)
    except:
        pass


def copy_file(src_path, dst_path):
    '''copy file from server to destination path in client'''
    src_path = convert_to_path(src_path)
    dst_path = convert_to_path(dst_path)

    # copy the file
    shutil.copy(src_path, dst_path)

    # check if the file was copied successfully
    if check_file_exist(dst_path):
        print("The file was copied successfully")
    else:
        print("The file could not be copied")


def send_file_to_folder(src_path, dst_dir):
    '''send a file to another directory in server'''

    src_path = convert_to_path(src_path)
    dst_dir = convert_to_path(dst_dir)

    # create the destination directory if it doesn't exist
    if not check_file_exist(dst_dir):
        os.mkdir(dst_dir)

    # move the file to the destination directory
    shutil.move(src_path, dst_dir)

    # check if the file was moved successfully
    dst_path = os.path.join(dst_dir, os.path.basename(src_path))

    if check_file_exist(dst_path):
        print("The file was moved successfully")
    else:
        print("The file could not be moved")


def delete_file(file_path):
    '''delete file in server'''
    file_path = convert_to_path(file_path)

    if check_file_exist(file_path):
        os.remove(file_path)
        return "File deleted"
    else:
        return "File not found"


if __name__ == "__main__":
    # show_directory_tree(root="~/Desktop/Gmail-Remote-Control", deep_level=2)
    # print(delete_file(file_path="~/Desktop/hi.txt"))
    # copy_file(src_path="~/Desktop/hi.txt", dst_path="~/hi2.txt")

    send_file_to_folder(src_path="~/Desktop/hi.txt",
                        dst_dir="~/Desktop/Gmail-Remote-Controls.txt")


# TODO: check in window

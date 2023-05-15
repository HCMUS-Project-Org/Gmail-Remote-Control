from itertools import islice
from pathlib import Path
import os
import shutil
import re
from . import shared_function as sf
#import shared_function as sf

# def check_path(path):
#     if "~" in path:
#         return sf.check_os() == "linux"
#     else:
#         return sf.check_os() == "window"


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
        result = ""

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
        result = str(dir_path.name)
        iterator = inner(dir_path, level=level)
        for line in islice(iterator, length_limit):
            result += "\n" + line
        if next(iterator, None):
            result += f'\n... length_limit, {length_limit}, reached, counted:'
        result += (f'\n{directories} directories' +
                   (f', {files} files' if files else ''))

        return result

    directory = sf.convert_to_path(root)

    result = ""

    try:
        for line in tree(directory, level=deep_level, limit_to_directories=True):
            result += line
        return result
    except:
        pass


def copy_file(src_path, dst_path):
    '''copy file from server to destination path in client'''
    src_path = sf.convert_to_path(src_path)
    dst_path = sf.convert_to_path(dst_path)

    # check if source exist
    if not sf.check_file_exist(src_path):
        return f'The file "{src_path}" does NOT exist'

    # create the destination directory if it doesn't exist
    if not sf.check_file_exist(dst_path):
        os.makedirs(dst_path)

    try:
        # copy the file
        shutil.copy(src_path, dst_path)

        # check if the file was copied successfully
        if sf.check_file_exist(dst_path):
            return f'The file "{src_path}" was COPIED to "{dst_path}" successfully'
        else:
            return f'The file "{src_path}" could NOT be COPIED'
    except:
        return f'The file {src_path} exist at destination or wrong file path'


def send_file_to_folder(src_path, dst_dir):
    '''send a file to another directory in server'''
    src_path = sf.convert_to_path(src_path)
    dst_dir = sf.convert_to_path(dst_dir)

    # check if source exist
    if not sf.check_file_exist(src_path):
        return f'The file "{src_path}" does NOT EXIST'

    # create the destination directory if it doesn't exist
    if not sf.check_file_exist(dst_dir):
        os.makedirs(dst_dir)

    try:
        # move the file to the destination directory
        shutil.move(src_path, dst_dir)

        # check if the file was moved successfully
        dst_path = os.path.join(dst_dir, os.path.basename(src_path))

        if sf.check_file_exist(dst_path):
            return f'The file "{src_path}" was SENDED to "{dst_dir}" SUCCESSFULLY'
        else:
            return f'The file "{src_path}" could NOT be SENDED to "{dst_dir}"'
    except:
        return f'The file {src_path} exist at destination or wrong file path'


def delete_file(file_path):
    '''delete file in server'''
    file_path = sf.convert_to_path(file_path)

    # check if the file was deleted successfully
    try:
        if sf.check_file_exist(file_path):
            os.remove(file_path)
            return f'The file "{file_path}" was DELETED'
        else:
            return f'The file "{file_path}" does NOT EXIST'
    except:
        return f'The file {file_path} wrong file path'


def parse_msg(msg):
    command = [x for x in msg.split(" - ")]
    return command


def parse_cmd(item):
    try:
        if "Show" in item:
            match = re.search(r'Show\[path:(.*), level:(\d+)\]', item)
            return match.group(1), int(match.group(2))

        elif "Delete file" in item:
            return re.search(r'Delete file\[path:(.*)\]', item).group(1), None

        # copy and send file
        else:
            match = re.search(r'\[source:(.*), destination:(.*)\]', item)
            return match.group(1), match.group(2)
    except:
        return False


def directory_manage(msg):
    command = parse_msg(msg)
    return_text = ""
    for item in command:
        result = ""
        param1, param2 = parse_cmd(item)
        if param1 == False:
            return_text += f"Wrong format at {item}"
            continue

        if "Show" in item:
            try:
                result = "Show directory tree:\n" + \
                    show_directory_tree(param1, param2)
            except:
                return_text += "\n" + "Cannot show directory at that folder"
                continue

        if "Copy file" in item:
            result = "Copy file:\n" + copy_file(param1, param2)

        if "Send file to folder" in item:
            result = "Send file to another folder:\n" + \
                send_file_to_folder(param1, param2)

        if "Delete file" in item:
            result = "Delete file:\n" + delete_file(param1)

        if result != "":
            return_text += "\n" + result

    return "<div class='mb-2'><b>Directory tree management:</b> " + return_text + "</div>"

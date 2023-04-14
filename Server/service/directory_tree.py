from itertools import islice
from pathlib import Path
import os
from shared_function import *


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

    directory = Path(os.path.expanduser(root))
    try:
        for line in tree(directory, level=deep_level, limit_to_directories=True):
            print(line)
    except:
        pass


if __name__ == "__main__":
    show_directory_tree(root="~/Desktop/Gmail-Remote-Control", deep_level=2)

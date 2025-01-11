
from typing import Dict, Tuple

import os
from pathlib import Path

from .aliases import PathLike


def mkdir(path: PathLike):
    """mkdir with parents"""
    Path(path).mkdir(parents=True, exist_ok=True)


def mkdir_of_file(file_path: PathLike):
    mkdir(Path(file_path).parent)


def read_text(result_path: PathLike, encoding: str = 'utf-8'):
    return Path(result_path).read_text(encoding=encoding)


def write_text(result_path: PathLike, text: str, encoding: str = 'utf-8'):
    Path(result_path).write_text(text, encoding=encoding)


def replace_string_parts(string: str, indexes_to_part: Dict[Tuple[int, int], str]) -> str:
    """
    replaces string parts according to map
    Args:
        string:
        indexes_to_part: dict { [start; end) -> new string }

    Returns:

    >>> ss = '0123456789'
    >>> replace_string_parts(ss, {(1, 3): '(1-3)', (4, 8): '(4-8)'})
    '0(1-3)3(4-8)89'
    """

    s = list(string)
    for (start, end), part in sorted(indexes_to_part.items(), reverse=True):
        s[start:end] = list(part)

    return ''.join(s)


def set_unix_sep(path: PathLike) -> str:
    """replaces backslash with unix /"""
    return str(path).replace(os.sep, '/')


def get_relative_path(path: PathLike, relative_to: PathLike) -> str:
    """
    returns relative path as string in unix-style format

    >>> assert get_relative_path('./a/b/c', './a') == 'b/c'
    >>> assert get_relative_path('./a', './a/b/c') == '../..'
    """
    return set_unix_sep(os.path.relpath(path, relative_to))


def isin(path: PathLike, parent: PathLike) -> bool:
    """
    checks whether the path is in other path
    Args:
        path: path to file or directory
        parent: the path to check whether it is its parent

    Returns:

    >>> assert isin('a/b/c', 'a/b')
    >>> assert isin('a/b/c', 'a')
    >>> assert not isin('a/b/c', 't/b')
    """
    return not get_relative_path(path, parent).startswith('..')

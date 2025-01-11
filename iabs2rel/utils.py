
from typing import Dict, Tuple

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


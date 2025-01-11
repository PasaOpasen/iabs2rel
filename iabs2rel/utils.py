
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





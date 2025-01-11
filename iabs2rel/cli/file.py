
from typing import Optional, Sequence


import sys
import argparse

from .utils import add_common_args
from ..main import IAbs2Rel


#region CLI

parser = argparse.ArgumentParser(
    prog='iabs2rel-file',
    description='Replaces absolute file imports to relative',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('source', type=str, help='python file path to replace imports')

parser.add_argument(
    '--destination', '-o', type=str, default=None,
    help='destination file; empty means to print to stdout'
)

add_common_args(parser)


def main(args: Optional[Sequence[str]] = None):
    kwargs = parser.parse_args(args or sys.argv[1:])

    i = IAbs2Rel(
        python_path=kwargs.python_path,
        allowed_paths=kwargs.allowed_paths,
        denied_paths=kwargs.denied_paths,
        loglevel=kwargs.loglevel
    )

    text, ok = i.file_abs2rel(kwargs.source, max_depth=kwargs.max_depth)

    dest = kwargs.destination
    if dest:
        from ..utils import write_text
        write_text(dest, text)
    else:
        print(text)


#endregion


if __name__ == '__main__':
    main()



from typing import Optional, Sequence


import sys
import argparse

from iabs2rel.cli.utils import add_common_args
from iabs2rel.main import IAbs2Rel


#region CLI

parser = argparse.ArgumentParser(
    prog='iabs2rel',
    description='Replaces absolute file imports to relative in all sources',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    'sources',
    type=str, nargs='+',
    help='paths to python files or directories with python files'
)

parser.add_argument(
    '--dry-run', '-n',
    action='store_true',
    help='Whether to run without performing file processing operations'
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

    i.abs2rel(
        kwargs.sources,
        max_depth=kwargs.max_depth,
        dry_run=kwargs.dry_run
    )


#endregion


if __name__ == '__main__':
    main()


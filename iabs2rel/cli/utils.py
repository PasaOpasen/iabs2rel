

import argparse

from ..aliases import LOGLEVEL_NAME


def add_common_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--python-path', '-p',
        nargs="+",
        type=str, default='',
        help=(
            'PYTHONPATH elements to resolve absolute imports; '
            'if nothing set then only CWD will be used; '
            'absolute imports that cannot be resolved will not be converted to relative'
        )
    )

    parser.add_argument(
        '--allowed-paths', '-a',
        nargs="+",
        type=str, default='',
        help=(
            'allowed import destination files/folder; '
            'if nothing set then any destination is allowed; '
            'if absolute import points not to allowed location it will not be converted to relative'
        )
    )

    parser.add_argument(
        '--denied-paths', '-e',
        nargs="+",
        type=str, default='',
        help=(
            'forbidden import destination files/folder; '
            'if absolute import points to forbidden location (even allowed) it will not be converted to relative'
        )
    )

    parser.add_argument(
        '--loglevel', '-l',
        choices=LOGLEVEL_NAME.__args__, type=str, default='DEBUG',
        help="using loglevel"
    )

    parser.add_argument(
        '--max-depth', '-d', type=int, default=1,
        help=(
            "max relative import depth; "
            "0 means only local imports to same package are allowed (start with 1 dot);"
            "1 means 0 + imports 1 level upper (start with 2 dots); "
            "higher values are available; "
            "values <0 disable any limits"
        )
    )



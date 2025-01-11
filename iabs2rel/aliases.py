
from typing import Union, Tuple, Literal, Dict
from typing_extensions import TypeAlias

import os


PathLike: TypeAlias = Union[str, os.PathLike]


ImportMatch: TypeAlias = Tuple[str, Tuple[int, int]]
"""
import string + [start; end) interval in the source code string
"""


LOGLEVEL: TypeAlias = Literal[0, 1, 2, 3, 4]
LOGLEVEL_NAME: TypeAlias = Literal['NO', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

level_to_name: Dict[LOGLEVEL, LOGLEVEL_NAME] = {
    0: 'NO', 1: 'ERROR', 2: 'WARNING', 3: 'INFO', 4: 'DEBUG'
}


name_to_level = {v: k for k, v in level_to_name.items()}


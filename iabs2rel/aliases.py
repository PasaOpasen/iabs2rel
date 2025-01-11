
from typing import Union, Tuple
from typing_extensions import TypeAlias

import os


PathLike: TypeAlias = Union[str, os.PathLike]

ImportMatch: TypeAlias = Tuple[str, Tuple[int, int]]
"""
import string + [start; end) interval in the source code string
"""


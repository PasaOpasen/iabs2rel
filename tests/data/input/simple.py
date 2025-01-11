
"""
simple script to check several import cases
"""

from typing import Set
from typing import List, Tuple

from typing_extensions import TypeAlias

import collections.abc

from collections import Counter
# from s import e


def func():
    from functools import lru_cache
    raise NotImplemented()


func()


def f():
    for _ in range(10):
        import re
        from itertools import product
        print()


f()

from iabs2rel.utils import read_text

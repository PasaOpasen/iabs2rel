
from typing import Iterable

import re

from .aliases import ImportMatch


def find_imports(code: str) -> Iterable[ImportMatch]:
    """searches for `from ... import` imports and returns matches items info"""

    for m in re.finditer(r"^\s*from\s+(\.*[_\w\d\.]*)\s+import\s", code, re.MULTILINE):
        s = m.start()
        e = m.end()
        g = m.group(1)
        st = code[s:e]
        i = st.index(g)
        s += i
        e = s + len(g)
        yield g, (s, e)




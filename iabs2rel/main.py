
from typing import Iterable, Sequence, Optional, List, Set, Union, Tuple

import os
import sys
from pathlib import Path
import re
import logging

from .aliases import ImportMatch, PathLike
from .utils import read_text, replace_string_parts, get_relative_path, is_allowed_path

logger = logging.getLogger('iabs2rel')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(levelname)s -- %(message)s'))
logger.handlers.append(handler)
logger.setLevel('DEBUG')

_FILE_END = '.py'
_PACKAGE_END = '/__init__.py'


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


def _find_import_source(
    i: str,
    python_path: Sequence[Path],
    allowed_paths: Optional[Set[str]] = None,
    denied_paths: Optional[Set[str]] = None
) -> Optional[Path]:
    """
    searches for the source file for the import
    Args:
        i: import string
        python_path: sequence of start paths to check
        allowed_paths:
        denied_paths:

    Returns:
        import source file if found else None
    """

    s = i.replace('.', '/')

    s_file = s + _FILE_END
    """import source in case of file """
    s_dir = s + _PACKAGE_END

    for p in python_path:
        for s in (s_file, s_dir):
            loc = p / s
            if loc.exists():
                return loc if is_allowed_path(loc, allowed_paths, denied_paths) else None


def _abs2rel(
    i: str,
    source: Path,
    python_path: Sequence[Path],
    max_depth: int = 0,
    allowed_paths: Optional[Set[str]] = None,
    denied_paths: Optional[Set[str]] = None
) -> str:
    """resolves import from the source file"""
    if i.startswith('.'):  # already relative
        return i

    try:
        dest = _find_import_source(i, python_path, allowed_paths=allowed_paths, denied_paths=denied_paths)
        if not dest:  # cannot be resolved
            return i
    except PermissionError:
        return i

    rel_path = get_relative_path(dest, relative_to=source.parent)

    if rel_path.endswith(_PACKAGE_END):
        rel_path = rel_path[:-len(_PACKAGE_END)]
    else:
        rel_path = rel_path[:-len(_FILE_END)]

    i_new = '.' + rel_path.replace('../', '.').replace('/', '.')  # replace slashes with dots

    if max_depth >= 0:  # limited
        dots_count: int = len(i_new) - len(i_new.lstrip('.'))
        if dots_count - 1 > max_depth:  # ignore too deep imports
            return i

    return i_new


def _filter_paths(
    paths: Optional[Iterable[PathLike]] = None,
    return_set: bool = False,
    allow_empty: bool = False,
    label: str = ''
) -> Union[List[Path], Set[str]]:
    """checks input paths for existence and filters them"""

    _paths = [
        t.absolute().resolve()
        for p in (paths or [])
        if (t := Path(p)).exists()
    ]
    if not _paths and (not allow_empty and paths):  # if all paths are filtered but is not okay
        raise ValueError(
            f"none of {label} paths exists (working directory = {os.getcwd()}): {[str(p) for p in paths]}"
        )

    if not return_set:
        return _paths
    return set(map(str, _paths))


def _filter_kwargs_paths(
    python_path: Optional[Iterable[PathLike]] = None,
    allowed_paths: Optional[Set[PathLike]] = None,
    denied_paths: Optional[Set[PathLike]] = None,
) -> Tuple[List[Path], Set[str], Set[str]]:
    return (
        _filter_paths(python_path, label='PYTHON_PATH'),
        _filter_paths(allowed_paths, return_set=True, label='allowed paths'),
        _filter_paths(denied_paths, allow_empty=True, return_set=True, label='denied paths'),
    )


def file_abs2rel(
    file: PathLike,
    max_depth: int = 0,
    python_path: Optional[Iterable[PathLike]] = None,
    allowed_paths: Optional[Set[PathLike]] = None,
    denied_paths: Optional[Set[PathLike]] = None,
    _filter_paths: bool = True
) -> str:

    if not python_path:
        python_path = [os.getcwd()]

    python_path, allowed_paths, denied_paths = _filter_kwargs_paths(
        python_path, allowed_paths, denied_paths
    )

    file = Path(file)
    text = read_text(file)

    replaces: List[ImportMatch] = []

    for i, (s, e) in find_imports(text):
        i_rel = _abs2rel(
            i, file, python_path, max_depth=max_depth,
            allowed_paths=allowed_paths, denied_paths=denied_paths
        )
        if i_rel != i:
            replaces.append(
                (i_rel, (s, e))
            )

    if not replaces:  # nothing to change
        return text

    return replace_string_parts(
        text,
        indexes_to_part={t: i for i, t in replaces}
    )


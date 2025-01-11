
from typing import Iterable, Sequence, Optional, List, Set, Union, Tuple, Dict

import os
import sys
from pathlib import Path
import re
import traceback


from .aliases import ImportMatch, PathLike, LOGLEVEL_NAME, name_to_level
from .utils import read_text, write_text, replace_string_parts, get_relative_path, is_allowed_path


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


class IAbs2Rel:

    def __init__(
        self,
        python_path: Optional[Iterable[PathLike]] = None,
        allowed_paths: Optional[Set[PathLike]] = None,
        denied_paths: Optional[Set[PathLike]] = None,
        loglevel: LOGLEVEL_NAME = 'DEBUG'
    ):
        self.loglevel = name_to_level[loglevel.upper()]

        if not python_path:
            self._verbose('add current working directory to PYTHON PATH cuz its empty', 'DEBUG')
            python_path = [os.getcwd()]

        self._python_path: List[Path] = self._filter_paths(python_path, label='PYTHON PATH')
        self._allowed_paths: Set[str] = self._filter_paths(allowed_paths, return_set=True, label='allowed paths')
        self._denied_paths: Set[str] = self._filter_paths(denied_paths, allow_empty=True, return_set=True, label='denied paths')

        self._cached_imports: Dict[str, Optional[Path]] = {}

    def _verbose(self, message: str, level: str):
        lv = self.loglevel
        if lv == 0:
            return

        if name_to_level[level.upper()] <= lv:
            print(f"{level.upper().ljust(7)} :: {message}")

    def _filter_paths(
        self,
        paths: Optional[Iterable[PathLike]] = None,
        return_set: bool = False,
        allow_empty: bool = False,
        label: str = ''
    ) -> Union[List[Path], Set[str]]:
        """checks input paths for existence and filters them"""

        _paths = []
        for p in (paths or []):
            t = Path(p)
            if not t.exists():
                self._verbose(
                    f"{label} path {str(p)} does not exist", 'WARNING'
                )
                continue
            _paths.append(t.absolute().resolve())

        if not _paths and (not allow_empty and paths):  # if all paths are filtered but is not okay
            raise ValueError(
                f"none of {label} paths exists (working directory = {os.getcwd()}): {[str(p) for p in paths]}"
            )

        self._verbose(
            f"using {label}: {[str(p) for p in _paths]}", 'DEBUG'
        )

        if not return_set:
            return _paths
        return set(map(str, _paths))

    def _find_import_source(self, i: str) -> Optional[Path]:
        """
        searches for the source file for the import
        Args:
            i: import string

        Returns:
            import source file if found else None
        """

        cached = self._cached_imports.get(i, ...)
        if cached is not Ellipsis:
            return cached

        s = i.replace('.', '/')

        s_file = s + _FILE_END
        """import source in case of file """
        s_dir = s + _PACKAGE_END

        for p in self._python_path:
            for s in (s_file, s_dir):
                loc = p / s
                if loc.exists():
                    if is_allowed_path(loc, self._allowed_paths, self._denied_paths):
                        self._verbose(f"import source found: {i} --> {str(loc)}", 'INFO')
                        v = loc
                    else:
                        self._verbose(f"import source found but not allowed: {i} --> {str(loc)}", 'INFO')
                        v = None

                    self._cached_imports[i] = v
                    return v

        self._verbose(f"no source found for import: {i}", 'DEBUG')
        self._cached_imports[i] = None
        return None

    def _abs2rel(
        self,
        i: str,
        source: Path,
        max_depth: int = -1,
    ) -> str:
        """resolves import from the source file"""
        if i.startswith('.'):  # already relative
            return i

        try:
            dest = self._find_import_source(i)
            if not dest:  # cannot be resolved
                return i
        except PermissionError:
            self._verbose(traceback.format_exc(), 'ERROR')
            return i

        rel_path = get_relative_path(dest, relative_to=source.parent)
        if rel_path == '__init__.py':
            self._verbose(
                f"will not resolve {i} as .", 'DEBUG'
            )
            return i

        if rel_path.endswith(_PACKAGE_END):
            rel_path = rel_path[:-len(_PACKAGE_END)]
        else:
            rel_path = rel_path[:-len(_FILE_END)]

        i_new = '.' + rel_path.replace('../', '.').replace('/', '.')  # replace slashes with dots

        if max_depth >= 0:  # limited
            dots_count: int = len(i_new) - len(i_new.lstrip('.'))
            if dots_count - 1 > max_depth:  # ignore too deep imports
                self._verbose(
                    f"will not resolve {i} as {i_new} cuz of max depth limit={max_depth}", 'DEBUG'
                )
                return i

        return i_new

    def file_abs2rel(self, file: PathLike, max_depth: int = -1) -> Tuple[str, bool]:
        """
        converts file abs imports to relative
        Args:
            file:
            max_depth: max relevance depth, -1 means unlimited

        Returns:
            - file original text or changed text
            - flag means the text is changed
        """

        file = Path(file)
        text = read_text(file)

        replaces: List[ImportMatch] = []
        to_resolve: Set[str] = set()

        for i, (s, e) in find_imports(text):
            i_rel = self._abs2rel(
                i, file, max_depth=max_depth,
            )
            if i_rel != i:
                replaces.append(
                    (i_rel, (s, e))
                )
                to_resolve.add(i)

        if not replaces:  # nothing to change
            self._verbose('no imports to resolve', 'INFO')
            return text, False

        self._verbose(
            f"next imports will be resolved: {to_resolve}", 'DEBUG'
        )
        self._verbose(
            f"resolving {len(replaces)} imports", 'INFO'
        )

        return replace_string_parts(
            text,
            indexes_to_part={t: i for i, t in replaces}
        ), True

    def abs2rel(self, paths: Union[PathLike, Iterable[PathLike]], max_depth: int = -1, dry_run: bool = False):
        """
        updates files abs imports to relative
        Args:
            paths: paths to python files or directories with files
            max_depth: max relevance depth, -1 means unlimited
            dry_run: whether to not change original files, just check for errors and produce output

        """

        if isinstance(paths, (str, Path)):
            paths = [paths]

        files: Set[str] = set()

        for p in paths:
            p = Path(p)
            assert p.exists(), p
            p = p.absolute().resolve()
            if p.is_file():
                assert p.suffix == '.py', p
                files.add(str(p))
            else:
                py_files = [str(p) for p in p.rglob('*.py')]
                if py_files:
                    files.update(py_files)
                else:
                    self._verbose(f"no python files found in folder {str(p)}", 'WARNING')

        self._verbose(f"===== processing {len(files)} *.py files =====", 'INFO')

        file2text = {}
        for f in sorted(files):
            self._verbose(f"\t<<<< processing {f} >>>>", 'INFO')
            text, changed = self.file_abs2rel(f, max_depth=max_depth)
            if changed:
                file2text[f] = text

        self._verbose(
            (
                f"update imports in next files ({len(file2text)} from {len(files)}):\n\t" +
                '\n\t'.join(sorted(file2text.keys()))
            ),
            'INFO'
        )
        if not dry_run:
            for f, t in file2text.items():
                write_text(f, t)


























from pathlib import Path
import pytest

from iabs2rel.aliases import PathLike
from iabs2rel.utils import read_text, read_json, write_text
from iabs2rel.main import find_imports, IAbs2Rel

from tests.config import DATA_DIR, PROJECT_DIR
from tests.utils import load_kwargs


def test_find_imports():
    text = read_text(DATA_DIR / 'input' / 'simple.py')

    imports = list(find_imports(text))

    for t, (s, e) in imports:
        assert text[s: e] == t, (t, s, e)

    assert [i[0] for i in imports] == [
        'typing',
        'typing',
        'typing_extensions',
        'collections',
        'functools',
        'itertools',
        'iabs2rel.utils'
    ]


_arg_files = list(
    (DATA_DIR / 'cases' / 'file').glob('*.json')
)


@pytest.mark.parametrize(
    'arg_file', _arg_files
)
def test_file_abs2rel(arg_file: PathLike):
    kwargs, func = load_kwargs(arg_file)

    resolver = IAbs2Rel(
        python_path=[PROJECT_DIR], **kwargs
    )

    text, ok = resolver.file_abs2rel(
        file=DATA_DIR / 'input/p/simple2.py', **func
    )

    target_file = DATA_DIR / 'output' / 'simple2' / (Path(arg_file).stem + '.py')

    # write_text(target_file, text)

    assert read_text(target_file) == text



















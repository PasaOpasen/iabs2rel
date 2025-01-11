
from iabs2rel.utils import read_text
from iabs2rel.main import find_imports

from tests.config import DATA_DIR


def test_find_imports():
    text = read_text(DATA_DIR / 'simple.py')

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



from pathlib import Path
import shutil
import pytest

from iabs2rel.aliases import PathLike
from iabs2rel.utils import read_text, write_text, rmdir, get_relative_path
from iabs2rel.main import IAbs2Rel

from tests.config import DATA_DIR, PROJECT_DIR
from tests.utils import load_kwargs


_arg_files = list(
    (DATA_DIR / 'cases' / 'file').glob('*.json')
)


@pytest.mark.parametrize(
    'arg_file', _arg_files
)
def test_dir_abs2rel(arg_file: PathLike):

    kwargs, func = load_kwargs(arg_file)

    resolver = IAbs2Rel(
        python_path=[PROJECT_DIR], **kwargs
    )

    in_dir = DATA_DIR / 'input'
    out_dir = DATA_DIR / 'tmp'
    rmdir(out_dir)
    shutil.copytree(in_dir, out_dir)

    for f in out_dir.rglob('*.py'):
        write_text(f, read_text(f).replace('tests.data.input.', 'tests.data.tmp.'))

    resolver.abs2rel(
        out_dir, **func
    )

    gold_dir = DATA_DIR / 'output/dir' / Path(arg_file).stem
    # rmdir(gold_dir)
    if not gold_dir.exists():
        shutil.copytree(out_dir, gold_dir)

    #
    # compare directories
    #
    py_files = [
        get_relative_path(p, gold_dir) for p in gold_dir.rglob('*.py')
    ]
    for f in py_files:
        gold = gold_dir / f
        current = out_dir / f
        assert current.exists(), current

        assert read_text(gold) == read_text(current)




from iabs2rel.utils import read_text
from iabs2rel.main import find_imports

find_imports(read_text(__file__))


from typing import Tuple, Dict, Any

from iabs2rel.aliases import PathLike
from iabs2rel.utils import read_json

from tests.config import DATA_DIR


def load_kwargs(path: PathLike) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    dct = read_json(path)

    kwargs = dct['obj']
    func = dct['func']

    # resolve paths
    for k, v in list(kwargs.items()):
        if v and k.endswith('paths'):
            kwargs[k] = [
                DATA_DIR / vv for vv in v
            ]

    return kwargs, func

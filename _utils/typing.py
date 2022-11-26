from pathlib import Path
from typing import *
from types import NoneType, UnionType, Any

# Universal
RealNumber = Union[int, float]
ListLike = Union[list, tuple]
PathLike = Union[str, bytes, int, Path]
Version = str
"""
Module that stores special types.    
"""

from pathlib import Path
from typing import *
from types import NoneType, UnionType

# Universal
RealNumber = Union[int, float]
ListLike = Union[list, tuple]
PathLike = Union[str, bytes, int, Path]
Version = str
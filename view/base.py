import os
import pickle
import pandas as pd

from pathlib import Path
from _utils.typing import PathLike
from _utils.validation import val_instance

from strategy.protocol import StrategyEvent


class Rview:
    @property
    def path(self) -> str:
        return self._path.__str__()
    
    @path.setter
    def path(self, _path: PathLike) -> None:
        val_instance(_path, PathLike)
        
        self._path = Path(_path)
        
        if not os.path.isfile(self._path):
            self._path.mkdir(parents=True)
    
    @path.deleter
    def path(self) -> None:
        raise ValueError(f"`Rview.path` can't be deleted, only overwritten.")
    
    def __init__(self, path: PathLike) -> None:
        self._path: Path = None
        
        self.path = path
        
    def read(self) -> None:
        pass
    
    def write(self) -> None:
        pass


class Viewer:
    def __init__(self) -> None:
        pass
    
    def render(self):
        pass
from typing import Any
from _utils.errors import RequiredOverwrite

class DataStream:
    def __init__(self) -> None:
        pass
    
    def request(self) -> Any:
        RequiredOverwrite("`request()` requires overwrite.")
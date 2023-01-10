from _utils.errors import RequiredOverwrite
from strategy.protocol import StrategyResponse

class Strategy:
    def __init__(self) -> None:
        pass
        
    def __feed__(self, *args) -> bool:
        return True

    def next(self, *args) -> StrategyResponse:
        raise RequiredOverwrite(f"`next()` requires overwrite.")

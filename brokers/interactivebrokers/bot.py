from _utils.validate import val_instance
from strategy.base import Strategy
from strategy.protocol.base import StrategyResponse


class Bot:
    @property
    def strategy(self) -> Strategy:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        val_instance(strategy, Strategy)
        
        self._strategy = strategy
        
    @strategy.deleter
    def strategy(self) -> None:
        raise AttributeError("Cannot delete `strategy` attribute.")
    
    def __init__(self, strategy: Strategy, data_stream: None, broker: None) -> None:
        self._strategy = None
        
        self.strategy = strategy
        
    def run() -> None:
        pass
    
    def handle(strategy_response: StrategyResponse) -> None:
        RequiredOverwrite("`handle()` requires overwrite.")
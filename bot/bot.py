from typing import Any
from _utils.errors import RequiredOverwrite
from _utils.validate import val_instance
from bot.datastream import DataStream
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
    
    @property
    def data_stream(self) -> DataStream:
        return self._data_stream
    
    @data_stream.setter
    def data_stream(self, data_stream: DataStream) -> None:
        val_instance(data_stream, DataStream)
        
        self._data_stream = data_stream
        
    @data_stream.deleter
    def data_stream(self) -> None:
        raise AttributeError("Cannot delete `data_stream` attribute.")
    
    
    def __init__(self, strategy: Strategy, data_stream: DataStream) -> None:
        self._strategy = None
        self._data_stream = None
        
        self.strategy = strategy
        self.data_stream = data_stream
        
    def run(self) -> None:
        while True:
            data: Any = self.data_stream.request()
            
            if self.strategy.__feed__(data):
                response: StrategyResponse = self.strategy.next(data)
                
                self.handle(response)
    
    def handle(strategy_response: StrategyResponse) -> None:
        RequiredOverwrite("`handle()` requires overwrite.")
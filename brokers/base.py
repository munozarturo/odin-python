from _utils.errors import MustOverrideError
from _utils.typing import Any, Callable
from _utils.validation import val_instance
from _utils.errors import Error

class BrokerError(Error):
    pass


class BotError(Error):
    pass


class Bot:
    @property
    def callback(self) -> Callable:
        return self.__callback
    
    @callback.setter
    def callback(self, callback: Callable) -> None:
        val_instance(callback, Callable)
        
        self.__callback = callback
        
    @callback.deleter
    def callback(self) -> None:
        self.__callback = lambda _: None
    
    def __init__(self, callback: Callable) -> None:
        self.callback = callback
    
    def run(*args) -> Any:
        raise MustOverrideError(f"Broker.run() must be overridden.")


class Broker:
    def place_order(self, *args) -> Any:
        raise MustOverrideError(f"Broker.place_order() must be overridden.")

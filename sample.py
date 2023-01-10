from _utils.validate import val_instance
from strategy import Strategy, StrategyResponse, Buy, Sell, Hold
import datetime as dt


class MyStrategy(Strategy):
    def __init__(self) -> None:
        self._ticks: list[float] = []
        
        self._moving_average: float = 0.0
        
        self._bought: bool = False
        self._hold_counter: int = 0

    def __feed__(self, time: dt.datetime, *args) -> bool:
        val_instance(time, dt.datetime)
        
        _time: dt.time = time.time()
        
        return _time > dt.time(9) and _time < dt.time(12)
    
    def next(self, time: dt.datetime, price: float) -> StrategyResponse:
        val_instance(time, dt.datetime)
        val_instance(price, float)
        
        self._ticks.append(price)
        
        if not self._bought:
            if len(self._ticks) < 20:
                return Hold()
            else:
                moving_average: float = sum(self._ticks[:20]) / 20
                
                if moving_average > self._moving_average:
                    self._moving_average = moving_average
                    self._bought = True
                    
                    return Buy()
        else:
            if self._hold_counter > 20:
                self._bought = False
                self._hold_counter = 0
                
                return Sell()
        
        if len(self._ticks) > 20:
            self._ticks.pop(0)
from _utils.validate import val_instance
from strategy import Strategy, Buy, Sell, Hold
import datetime as dt


class SampleStrategy(Strategy):
    def __init__(self) -> None:
        """
        Create an instance of SampleStrategy.
        """
        
        # list of ticks
        self._ticks: list[float] = []
        
        # moving average of the last 20 ticks
        self._moving_average_last_20: float = None
        
        # boolean to store whether a buy response has been returned
        self._buy_response_sent: bool = False
        # counter to store how many ticks the strategy has been holding
        self._hold_after_buy_counter: int = 0

    def __feed__(self, time: dt.datetime, *args) -> bool:
        """
        Returns whether to call the next() method.

        Args:
            time (dt.datetime): The time of the datapoint.

        Returns:
            bool: True if the next() method should be called, False otherwise.
        """
        
        # validate that a datetime has been passed
        val_instance(time, dt.datetime) # this line can be removed for the sake of performance
        
        # get the time of the datapoint
        _time: dt.time = time.time()
        
        # only feed if the time is between 9:00 and 12:00
        return _time > dt.time(9) and _time < dt.time(12)
    
    def next(self, time: dt.datetime, price: float) -> Buy | Sell | Hold:
        """
        Method to mimick the passing of the next tick.

        Args:
            time (dt.datetime): time of the datapoint.
            price (float): price of the datapoint.

        Returns:
            Buy | Sell | Hold: command.
        """
        
        # input validation (can be removed for performance)
        val_instance(time, dt.datetime)
        val_instance(price, float)
        
        # add out datapoint to the ticks
        self._ticks.append(price)
        
        # if there has not been a buy condition look for one
        if not self._buy_response_sent:
            # if there aren't enough datapoints to calculate the moving average of the last 20 ticks then hold()
            if len(self._ticks) < 20:
                return Hold()
            else:
                # calculate the moving average of the last 20 ticks
                moving_average_last_20: float = sum(self._ticks[:20]) / 20
                
                # if this is the first time the moving average has been calculated then hold()
                if self._moving_average_last_20 is None:
                    self._moving_average_last_20 = moving_average_last_20
                    
                    return Hold()
                else:
                    # if the moving average is greater than the moving average the last tick
                    if moving_average_last_20 > self._moving_average_last_20:
                        # update the moving average
                        self._moving_average_last_20 = moving_average_last_20
                        # store that a buy response has been sent
                        self._buy_response_sent = True
                        
                        # return a buy response
                        return Buy()
        else:
            # if a buy response has been sent then hold() for 20 ticks
            if self._hold_after_buy_counter > 20:
                # reset the strategy variables so that the strategy will buy again
                self._moving_average_last_20 = None
                self._buy_response_sent = False
                self._hold_after_buy_counter = 0
                
                # return a sell response
                return Sell()
            
            # increment the hold counter
            self._hold_after_buy_counter += 1
        
        # if the lenght of the ticks is greater than 20, clear the last one
        if len(self._ticks) > 20:
            self._ticks.pop(0)
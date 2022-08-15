import datetime as dt
from math import isnan
from pathlib import Path
from types import NoneType
from typing import SupportsInt
import json

from _utils.typing import PathLike
from _utils.validation import LogWarning, val_instance
from _utils.time import parse_time

nan = float("nan")

LOCAL_TIMEZONE = dt.datetime.now(dt.timezone.utc).astimezone().tzinfo

# todo: implement strategyevent
class StrategyEvent:
    def __init__(self) -> None:
        raise NotImplementedError()


class StrategyResponse:
    @property
    def time(self) -> dt.datetime | dt.time | dt.date | NoneType:
        return self._time

    @time.setter
    def time(self, _time: dt.datetime | dt.time | dt.date | str | NoneType) -> None:
        val_instance(_time, (dt.datetime, dt.time, dt.date, str, NoneType))

        if not _time is None:
            if isinstance(_time, str):
                if _time in ("now", "auto"):
                    self._time = dt.datetime.now(tz=LOCAL_TIMEZONE)
                else:
                    self._time = parse_time(_time)
            else:
                self._time = _time
        else:
            self._time = nan

    @time.deleter
    def time(self) -> None:
        del self._time
        self._time = nan

    @property
    def price(self) -> float | int | NoneType:
        return self._price

    @price.setter
    def price(self, _price: float | int | NoneType) -> None:
        val_instance(_price, (float, int, NoneType))

        if not _price is None:
            if _price < 0:
                LogWarning(
                    f"less than 0 `_price` likely to cause runtime errors.")

            self._price = _price
        else:
            self._price = nan

    @price.deleter
    def price(self) -> None:
        del self._time
        self._time = None

    @property
    def command(self) -> str:
        return self._command

    @command.setter
    def command(self, _command: str | int | NoneType) -> None:
        val_instance(_command, (str, int, NoneType))

        __commands = ("HOLD", "BUY", "SELL")

        if not _command is None:
            if isinstance(_command, int):
                if not _command in (0, 1, 2):
                    raise ValueError(
                        f"expected 0, 1, or 2 for `_command` got '{_command}'. 0: 'HOLD', 1: 'BUY', 2: 'SELL'")

                self._command = __commands[_command]
            elif isinstance(_command, str):
                _command = _command.upper()

                if not _command in __commands:
                    raise ValueError(
                        f"expected 'HOLD', 'BUY', or 'SELL' for `_command` got '{_command}'.")

                self._command = _command
        else:
            self._command = "HOLD"

    @command.deleter
    def command(self) -> None:
        raise ValueError(
            f"`_command` can't be deleted. overwrite only class variable.")

    @property
    def ticker(self) -> str | NoneType:
        return self._ticker

    @ticker.setter
    def ticker(self, _ticker: str | NoneType):
        val_instance(_ticker, (str, NoneType))

        if not _ticker is None:
            self._ticker = _ticker.upper()
        else:
            self._ticker = None

    @ticker.deleter
    def ticker(self):
        del self._ticker
        self._ticker = None

    @property
    def exchange(self) -> str | NoneType:
        return self._exchange

    @exchange.setter
    def exchange(self, _exchange: str | NoneType):
        val_instance(_exchange, (str, NoneType))

        if not _exchange is None:
            self._exchange = _exchange.upper()
        else:
            self._exchange = None

    @exchange.deleter
    def exchange(self):
        del self._exchange
        self._exchange = None

    @property
    def uid(self) -> int | NoneType:
        return self._uid

    @uid.setter
    def uid(self, _uid: int | NoneType) -> None:
        val_instance(_uid, (int, SupportsInt, NoneType))

        if not _uid is None:
            if isinstance(_uid, SupportsInt):
                _uid = int(_uid)

            self._uid = _uid
        else:
            self._uid = None

    @uid.deleter
    def uid(self) -> None:
        del self._uid
        self._uid = None

    def __init__(self, time: dt.datetime | dt.time | dt.date | str | NoneType = None, price: float | int | NoneType = None, command: str | int | NoneType = None, ticker: str | NoneType = None, exchange: str | NoneType = None, uid: int | NoneType = None) -> None:
        """
        Generate a StrategyResponse object desgined to represent a 'buy', 'sell', or 'hold' order.

        Args:
            time (dt.datetime | dt.time | dt.date | str | NoneType, optional): time of order creation (if str will be parsed to dt.datetime [not recommended]). Defaults to None, can be 'auto' or 'now' to set order time as current time.
            price (float | int | NoneType, optional): price at order creation. Defaults to None, if None represented as 'nan'.
            command (str | int | NoneType, optional): 'buy', 'sell' or 'hold'. Defaults to 'hold.
            ticker (str | NoneType, optional): ticker of stock to be bought. Defaults to None.
            exchange (str | NoneType, optional): exchange at which the stock is to be bought. Defaults to None.
            uid (int | NoneType, optional): unique id used to pair with 'sell' and 'hold' commands. Defaults to None, will not be paired.
        """

        self._time = None
        self._price = None
        self._command = None
        self._ticker = None
        self._exchange = None
        self._uid = None

        self.time = time
        self.price = price
        self.command = command
        self.ticker = ticker
        self.exchange = exchange
        self.uid = uid

    def __hash__(self) -> int:
        return self._uid

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return (self._time == __o._time and
                self._price == __o._price and
                self._command == __o._command and
                self._ticker == __o._ticker and
                self._exchange == __o._exchange and
                self._uid == __o._uid)

    def __str__(self) -> str:
        _str = ""

        if not self._time is None:
            _str += f"{self._time.isoformat()} "

        _str += f"{self._command}"

        if not self._uid is None:
            _str += f"[{self._uid}]"

        if not (self._ticker is None or self._exchange is None):
            _str += f": "

        if not self._ticker is None:
            _str += f"{self._ticker}"

        if not self._exchange is None:
            _str += f" ({self._exchange})"

        if not isnan(self._price):
            _str += f" @ ${self._price}"

        return _str

    def as_dict(self) -> dict:
        return self.__dict__()

    def __dict__(self) -> dict:
        __dict: dict = {
            "time": self.time,
            "price": self.price,
            "command": self.command,
            "ticker": self.ticker,
            "exchange": self.exchange,
            "uid": self.uid
        }

        if not self.time is None:
            __dict["time"] = self.time.isoformat()

        if not isnan(self.price):
            __dict["price"] = self.price

        __dict["command"] = self.command

        if not self.ticker is None:
            __dict["ticker"] = self.ticker

        if not self.exchange is None:
            __dict["exchange"] = self.exchange

        if not self.uid is None:
            __dict["uid"] = self.uid

        return __dict

    def to_json(self, __json: PathLike, exist_ok: bool = False, allow_nan: bool = False, indent: bool = False) -> None:
        """
        convert the StrategyResponse to a json object stored at `__json`.

        Args:
            __json (PathLike): path to be stored at.
            exist_ok (bool, optional): if `__json` doesn't exist as a path it will be generated. if it already exists it will be overwritten if `exist_ok` is True. Defaults to False.
            allow_nan (bool, optional): allow 'NaN' values in the json. Defaults to False.
            indent (bool, optional): indent json file. Defaults to False.
        """
        
        val_instance(__json, PathLike)
        val_instance(allow_nan, bool)
        val_instance(indent, bool)

        __json = Path(__json)

        __json.mkdir(parents=True, exist_ok=exist_ok)

        with open(__json, "w") as f:
            json.dump(self.__dict__(), f, allow_nan=allow_nan, indent=indent)


def response_from_dict(__dict: dict) -> StrategyResponse:
    """
    Generate a StrategyResponse object from a dict of that class.
    Unrecognized keys will be ignored.

    Args:
        __dict (dict): StrategyResponse dict.

    Returns:
        StrategyResponse
    """
    
    val_instance(__dict, dict)

    if "time" in __dict:
        _time = __dict["time"]

    if "price" in __dict:
        _price = __dict["price"]

    if "command" in __dict:
        _command = __dict["command"]

    if "ticker" in __dict:
        _ticker = __dict["ticker"]

    if "exchange" in __dict:
        _exchange = __dict["exchange"]

    if "uid" in __dict:
        _uid = __dict["uid"]

    return StrategyResponse(
        time=_time,
        price=_price,
        command=_command,
        ticker=_ticker,
        exchange=_exchange,
        uid=_uid
    )


def response_from_json(__json: PathLike) -> StrategyResponse:
    """
    Generate a StrategyResponse object from a json file of that class.
    Unrecognized keys will be ignored.

    Args:
        __json (PathLike): path to StrategyResponse json.

    Returns:
        StrategyResponse
    """
    
    val_instance(__json, PathLike)

    with open(__json, "r") as f:
        return response_from_dict(json.load(f))


class Hold(StrategyResponse):
    """
    Generate a StrategyResponse object desgined to represent a 'hold' order.

    Args:
        time (dt.datetime | dt.time | dt.date | str | NoneType, optional): time of order creation (if str will be parsed to dt.datetime [not recommended]). Defaults to None, can be 'auto' or 'now' to set order time as current time.
        price (float | int | NoneType, optional): price at order creation. Defaults to None, if None represented as 'nan'.
        ticker (str | NoneType, optional): ticker of stock to be bought. Defaults to None.
        exchange (str | NoneType, optional): exchange at which the stock is to be bought. Defaults to None.
        uid (int | NoneType, optional): unique id used to pair with 'sell' and 'hold' commands. Defaults to None, will not be paired.
    """
    
    def __init__(self, time: dt.datetime | dt.time | dt.date | NoneType = None, price: float | int | NoneType = None, ticker: str | NoneType = None, exchange: str | NoneType = None, uid: int | NoneType = None) -> None:
        super().__init__(time, price, "HOLD", ticker, exchange, uid)


class Buy(StrategyResponse):
    """
    Generate a StrategyResponse object desgined to represent a 'buy' order.

    Args:
        time (dt.datetime | dt.time | dt.date | str | NoneType, optional): time of order creation (if str will be parsed to dt.datetime [not recommended]). Defaults to None, can be 'auto' or 'now' to set order time as current time.
        price (float | int | NoneType, optional): price at order creation. Defaults to None, if None represented as 'nan'.
        ticker (str | NoneType, optional): ticker of stock to be bought. Defaults to None.
        exchange (str | NoneType, optional): exchange at which the stock is to be bought. Defaults to None.
        uid (int | NoneType, optional): unique id used to pair with 'sell' and 'hold' commands. Defaults to None, will not be paired.
    """
    
    def __init__(self, time: dt.datetime | dt.time | dt.date | NoneType = None, price: float | int | NoneType = None, ticker: str | NoneType = None, exchange: str | NoneType = None, uid: int | NoneType = None) -> None:
        super().__init__(time, price, "BUY", ticker, exchange, uid)


class Sell(StrategyResponse):
    """
    Generate a StrategyResponse object desgined to represent a 'sell' order.

    Args:
        time (dt.datetime | dt.time | dt.date | str | NoneType, optional): time of order creation (if str will be parsed to dt.datetime [not recommended]). Defaults to None, can be 'auto' or 'now' to set order time as current time.
        price (float | int | NoneType, optional): price at order creation. Defaults to None, if None represented as 'nan'.
        ticker (str | NoneType, optional): ticker of stock to be bought. Defaults to None.
        exchange (str | NoneType, optional): exchange at which the stock is to be bought. Defaults to None.
        uid (int | NoneType, optional): unique id used to pair with 'sell' and 'hold' commands. Defaults to None, will not be paired.
    """
    
    def __init__(self, time: dt.datetime | dt.time | dt.date | NoneType = None, price: float | int | NoneType = None, ticker: str | NoneType = None, exchange: str | NoneType = None, uid: int | NoneType = None) -> None:
        super().__init__(time, price, "SELL", ticker, exchange, uid)

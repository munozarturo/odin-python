import datetime as dt
from abc import ABC
from math import isnan
from types import NoneType
from typing import SupportsInt

from _utils.validate import LogWarning, val_instance

nan = float("nan")


# todo: implement strategyevent
class StrategyEvent:
    def __init__(self) -> None:
        raise NotImplementedError()


class StrategyResponse:
    @property
    def time(self) -> dt.datetime | dt.time | dt.date | NoneType:
        return self._time

    @time.setter
    def time(self, _time: dt.datetime | dt.time | dt.date | NoneType) -> None:
        val_instance(_time, (dt.datetime, dt.time, dt.date, NoneType))

        if not _time is None:
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

    def __init__(self, time: dt.datetime | dt.time | dt.date | NoneType = None, price: float | int | NoneType = None,
                 command: str | int | NoneType = None, ticker: str | NoneType = None, exchange: str | NoneType = None,
                 uid: int | NoneType = None) -> None:
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

    def as_dict(self):
        raise NotImplementedError()

    def to_json(self):
        raise NotImplementedError()


class Hold(StrategyResponse):
    def __init__(self, time: dt.datetime | dt.time | dt.date | NoneType = None, price: float | int | NoneType = None,
                 ticker: str | NoneType = None, exchange: str | NoneType = None, uid: int | NoneType = None) -> None:
        super().__init__(time, price, "HOLD", ticker, exchange, uid)


class Buy(StrategyResponse):
    def __init__(self, time: dt.datetime | dt.time | dt.date | NoneType = None, price: float | int | NoneType = None,
                 ticker: str | NoneType = None, exchange: str | NoneType = None, uid: int | NoneType = None) -> None:
        super().__init__(time, price, "BUY", ticker, exchange, uid)


class Sell(StrategyResponse):
    def __init__(self, time: dt.datetime | dt.time | dt.date | NoneType = None, price: float | int | NoneType = None,
                 ticker: str | NoneType = None, exchange: str | NoneType = None, uid: int | NoneType = None) -> None:
        super().__init__(time, price, "SELL", ticker, exchange, uid)


class Trade:
    def __init__(self) -> None:
        pass

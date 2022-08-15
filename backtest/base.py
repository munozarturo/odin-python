from typing import Any, Iterable
import pandas as pd

from strategy.protocol import StrategyResponse, Trade


class Trades:
    @property
    def trades(self) -> pd.DataFrame:
        return self._trades

    @trades.setter
    def trades(self, _trades: Any | pd.DataFrame | Iterable[StrategyResponse] | Iterable[Trade]) -> None:
        self._trades = _trades

    @trades.deleter
    def trades(self) -> None:
        del self._trades
        self._trades = None

    def __init__(self) -> None:
        self._trades: pd.DataFrame

    def add(self, trade: Trade):
        pass

    def remove(self, query: Any):
        pass

    def find(self, query: Any):
        pass

    def as_list(self) -> list:
        pass

    def to_csv(self) -> None:
        pass

    def to_pickle(self) -> None:
        pass

    def info(self, verbose: bool = False) -> dict | str:
        pass


def from_responses() -> Trades:
    pass


def from_results() -> Trades:
    pass

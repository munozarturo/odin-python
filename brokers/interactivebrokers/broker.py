from _utils.errors import ReadOnlyPropertyError
from brokers.base import Broker, Dispatch, uids_range
from brokers.interactivebrokers.base import InteractiveBrokersDispatch
from _utils.validation import val_instance
from ib_insync import *
import ib_insync


# todo: Finish documentation


class InteractiveBrokersBroker(Broker):
    def getib(self) -> IB:
        return self.__ib

    @property
    def trades(self) -> list[Trade]:
        return self.__trades

    @trades.setter
    def trades(self, _trades: None) -> None:
        raise ReadOnlyPropertyError(f"`trades` is a read-only property.")

    @trades.deleter
    def trades(self) -> None:
        raise ReadOnlyPropertyError(f"`trades` is a read-only property.")

    def __init__(self, host: str = "127.0.0.1", port: int = 7497, timeout: float = 4, account: str = "") -> None:
        val_instance(host, str)
        val_instance(port, int)
        val_instance(timeout, (float, int))
        val_instance(account, str)

        self.__dispatch = InteractiveBrokersDispatch

        self.__ib = ib_insync.IB()

        # connect to IB object
        self.__uid = self.__dispatch.allocate_uid()
        self.__ib.connect(host=host, port=port, clientId=self.__uid,
                          timeout=timeout, readonly=True, account=account)

        self.__trades: list[Trade] = []

    def place_order(self, contract: Contract, order: Order) -> Trade:
        val_instance(contract, Contract)
        val_instance(order, Order)

        _trade = self.__ib.placeOrder(contract, order)
        self.__trades.append(_trade)

        return _trade

    def cancel_order(self, order: Order) -> Trade:
        val_instance(order, Order)

        _trade = self.__ib.cancelOrder(order)
        self.__trades.remove(_trade)

        return _trade

    def __del__(self):
        """
        Free the UID being used by the Broker and disconnect from the Interactive Brokers socket.
        """
        self.__dispatch.free_uid(self.__uid)
        self.__ib.disconnect()

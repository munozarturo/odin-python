from _utils.errors import MustOverrideError


# todo: Make objects that can inherit from Dispatch and still work.


class Error(Exception):
    pass


class DispatchError(Error):
    pass


class BrokerError(Error):
    pass


class Bot:
    pass


class Broker:
    def place_order(*args) -> Any:
        raise MustOverrideError(f"{self.__class__.__name__}.place_order")

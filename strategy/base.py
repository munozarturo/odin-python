from _utils.validate import val_instance
from strategy.protocol import StrategyResponse

# todo: rewrite docs


class RequiredOverwrite(Exception):
    """ Base class for classes that require an overwrite. """
    pass


class Strategy:
    def __init__(self) -> None:

        self.__initvars__()

    def __feed__(self, *args) -> bool:
        return True

    def next(self, *args) -> StrategyResponse:
        raise RequiredOverwrite(f"`next()` requires overwrite.")
